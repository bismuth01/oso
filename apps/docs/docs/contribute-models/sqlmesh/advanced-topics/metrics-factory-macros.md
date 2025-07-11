---
title: Metrics Factory Macros
sidebar_position: 2
---

:::info
This document provides a comprehensive reference for the special macros used in OSO's metrics factory. These macros are essential for creating dynamic and consistent metrics.
:::

## Special Macros

OSO has a set of special macros that can be used in metrics definitions to simplify the process of generating metrics. Here are some of the most commonly used macros:

### `@metrics_peer_ref`

Reference a different metrics table that is being generated by the timeseries
metrics factory. This should only be used if the table dependency is also
defined in the same factory.

**Parameters**:

- `name` - The name of the table dependency
- `entity_type` - _optional_ - The entity type for the current peer reference.
  Defaults to the entity type used in the current metric
- `window` - _optional_ - The size of the table dependency's window. If
  `time_aggregation` is not set, this and `unit` must be set.
- `unit` - _optional_ - The unit of the table dependency's window. If
  `time_aggregation` is not set, this and the `window` must be set.
- `time_aggregation` - _optional_ - The time aggregation used (one of `daily`,
  `weekly`, `monthly`). If this is not set then `window` and `unit` must be set.

_NOTE: Optional parameters should use the "kwargs" syntax in sqlmesh dialect.
This looks like `key := 'value'`_

**Usage**:

Select star from a dependent table that matches the current rolling window settings:

```sql
SELECT *
-- As noted in the docs the `entity_type` is inferred from the settings on this metric
FROM @metrics_peer_ref(`dep`, window := @rolling_window, unit := @rolling_unit)
```

Select star from a dependent table that matches the current time aggregation
settings, but only for the `artifact` entity type.

```sql
SELECT *
FROM @metrics_peer_ref(`dep`, entity_type := 'artifact', time_aggregation := @time_aggregation)
```

### `@metrics_sample_date`

Derives the correct sample date for a metric based on the metric type (normal
aggregation or rolling window aggregation). This is essential to use for first
order metrics.

**Usage**:

```
@metrics_sample_date(event_table_source.event_table_date_column)
```

The passed in date should be the date column of a given time series event
source. In all cases that must use this, this is just
`int_events_daily_to_artifact.bucket_day`.

### `@metric_start` and `@metric_end`

For rolling windows or time aggregations that have boundaries that correlate to
times, these provide the proper time ranges. So for a rolling window of 30 days
this will give a 30 day time window where the start days is 30 days _before_ the
interval for the current increment of the given model. So for example if the
increment is `2024-01-30` the start will be `2024-01-01` and the end will be
`2024-01-30`. These macros take a single argument which is the data type to use
for the returned value.

**Usage**:

For a date

```
@metrics_start(DATE)
```

For a timestamp (the value you use for type will depend on the dialect you're
using)

```
@metrics_start(TIMESTAMP)
```

### `@metrics_name`

The metrics name is used to generate a name for a given metric. By default this
can be used without any arguments and the metrics model factory will
automatically assign a metric name. However in cases like the developer
classifications we want to create multiple types of metrics in a given query. We
can accomplish simply using this macro. The first argument is the "prefix" name
of the metric. This macro will then generate the appropriate suffix. For time
aggregations this will simply be something like `daily`, `weekly`, or `monthly`.
For rolling windows this will be something like, `_over_30_days` or
`_over_3_months` (the exact string depends on the rolling window configuration).

### `@metrics_entity_type_col`

Provides a way to reference the generated column for a given entity type in a
metrics model. This is required because the metrics definition only acts as the
starting point of a metric from the perspective of an artifact. To get metrics
for projects and collections we need this macro while we aren't doing a fully
generic semantic model. be entity column name based on the currently queried
entity type. When queries are being automatically generated, entity types are
changed so the column used to reference the entity column also changes. This
macro allows for the queries to succeed by accepting a format string where the
variable `entity_type` referenced as `{entity_type}` in the format string is
interpreted as the current entity type (`artifact`, `project`, `collection`).

**Usage**:

```
@metrics_entity_type_col("to_{entity_type}_id")
```

### `@metrics_entity_type_alias`

Like, `@metric_entity_type_col` but programmatically aliases any input
expression with one that derives from the entity type.

**Usage**:

```
@metrics_entity_type_alias(some_column, 'some_{entity_type}_column")
```

### `@relative_window_sample_date`

_WARNING: Interface likely to change_

Gets a rolling window sample date relative to the a passed in base date. This is
intended to allow comparison of multiple rolling intervals to each other. This
doesn't specifically use the rolling window parameters of a table dependency
(that will likely change in the future), but is instead just a convenience
function to calculate the correct dates that would be used to make that rolling
window comparison. We calculate a relative window's sample date using this
formula:

```
$base + INTERVAL $relative_index * $window $unit
```

_Note: The dollar sign `$` is used here to signify that this is a parameter in the above
context_

Inherently, this won't, for now, work on custom unit types as the interval must
be a valid SQL interval type. Also note, the base should almost _always_ be the
`@metrics_end` date.

**Parameters**:

- `base` - The date time to use as the basis for this relative sample date
  calculation
- `window` - The rolling window size of the table we'd like to depend on
- `unit` - The rolling window unit of the table we'd like to depend on
- `relative_index` - The relative index to the current interval. This allows us
  to look forward or back a certain number of rolling intervals in an upstream
  table.

**Usage**:

To get the date for the current, the last, and the second to last sample date of
a 90 day rolling window, you could do the following:

```sql
SELECT
  -- Relative index 0. This just becomes 2024-01-01
  @relative_window_sample_date('2024-01-01', 90, 'day', 0)
  -- Relative index -1. This becomes 2023-10-03
  @relative_window_sample_date('2024-01-01', 90, 'day', -1)
  -- Relative index -2. This becomes 2023-07-05
  @relative_window_sample_date('2024-01-01', 90, 'day', -2)
```
