import textwrap

from ..definition import (
    Dimension,
    Measure,
    Model,
    Registry,
    Relationship,
    RelationshipType,
)


def register_entities(registry: Registry, catalog_name: str = "iceberg"):
    # ============================================"
    # CORE ENTITIES
    # ============================================"

    registry.register(
        Model(
            name="artifacts",
            table=f"{catalog_name}.oso.artifacts_v1",
            description=textwrap.dedent(
                """
                An artifact. This is the smallest atom of an acting entity in
                OSO. Artifacts are usually repositories, blockchain addresses,
                or some representation of a user. Artifacts do not generally
                represent a group of any kind, but rather a single entity.
                """
            ),
            dimensions=[
                Dimension(
                    name="artifact_id",
                    description="The unique identifier for the artifact",
                    column_name="artifact_id",
                ),
                Dimension(
                    name="artifact_source_id",
                    description="The native identifier for the artifact from the source",
                    column_name="artifact_source_id",
                ),
                Dimension(
                    name="artifact_source",
                    description="The original source of the artifact (GITHUB, NPM, DEFILLAMA)",
                    column_name="artifact_source",
                ),
                Dimension(
                    name="artifact_namespace",
                    description="The grouping or namespace of the artifact",
                    column_name="artifact_namespace",
                ),
                Dimension(
                    name="artifact_name",
                    description="The name of the artifact",
                    column_name="artifact_name",
                ),
            ],
            primary_key="artifact_id",
            relationships=[
                Relationship(
                    name="by_project",
                    source_foreign_key="artifact_id",
                    ref_model="artifacts_by_project",
                    ref_key="artifact_id",
                    type=RelationshipType.ONE_TO_MANY,
                ),
                Relationship(
                    name="by_collection",
                    source_foreign_key="artifact_id",
                    ref_model="artifacts_by_collection",
                    ref_key="artifact_id",
                    type=RelationshipType.ONE_TO_MANY,
                ),
                Relationship(
                    name="by_user",
                    source_foreign_key="artifact_id",
                    ref_model="artifacts_by_user",
                    ref_key="artifact_id",
                    type=RelationshipType.ONE_TO_MANY,
                ),
            ],
            measures=[
                Measure(
                    name="count",
                    description="The number of artifacts",
                    query="COUNT(self.artifact_id)",
                ),
                Measure(
                    name="distinct_count",
                    description="The number of distinct artifacts",
                    query="COUNT(DISTINCT self.artifact_id)",
                ),
            ],
        )
    )

    registry.register(
        Model(
            name="projects",
            table=f"{catalog_name}.oso.projects_v1",
            description=textwrap.dedent(
                """
                A project is a collection of related artifacts. A project is
                usually, but not limited to, some kind of organization, company,
                or group that controls a set of artifacts.
                """
            ),
            dimensions=[
                Dimension(
                    name="project_id",
                    description="The unique identifier for the project, as generated by OSO",
                    column_name="project_id",
                ),
                Dimension(
                    name="project_source",
                    description="The source of the project (OSS_DIRECTORY, OP_ATLAS)",
                    column_name="project_source",
                ),
                Dimension(
                    name="project_namespace",
                    description="The namespace of the project within the source",
                    column_name="project_namespace",
                ),
                Dimension(
                    name="project_name",
                    description="The project slug or other name given to the project",
                    column_name="project_name",
                ),
                Dimension(
                    name="display_name",
                    description="The display name of the project, more human-readable",
                    column_name="display_name",
                ),
                Dimension(
                    name="description",
                    description="A short description of the project",
                    column_name="description",
                ),
            ],
            primary_key="project_id",
            relationships=[
                Relationship(
                    name="by_collection",
                    source_foreign_key="project_id",
                    ref_model="projects_by_collection",
                    ref_key="project_id",
                    type=RelationshipType.ONE_TO_MANY,
                ),
            ],
            measures=[
                Measure(
                    name="count",
                    description="The number of projects",
                    query="COUNT(self.project_id)",
                ),
                Measure(
                    name="distinct_count",
                    description="The number of distinct projects",
                    query="COUNT(DISTINCT self.project_id)",
                ),
            ],
        )
    )

    registry.register(
        Model(
            name="collections",
            table=f"{catalog_name}.oso.collections_v1",
            description=textwrap.dedent(
                """
                A collection is a group of related projects. A collection is an
                arbitrary grouping of projects. Sometimes these groupings are
                used to group things together by some common dependency tree or
                some specific community known to OSO.
                """
            ),
            dimensions=[
                Dimension(
                    name="collection_id",
                    description="The unique identifier for the collection",
                    column_name="collection_id",
                ),
                Dimension(
                    name="collection_source",
                    description="The source of the collection (OP_ATLAS, OSS_DIRECTORY)",
                    column_name="collection_source",
                ),
                Dimension(
                    name="collection_namespace",
                    description="The grouping or namespace of the collection",
                    column_name="collection_namespace",
                ),
                Dimension(
                    name="collection_name",
                    description="The name of the collection, such as an ecosystem name",
                    column_name="collection_name",
                ),
                Dimension(
                    name="display_name",
                    description="The display name of the collection, human-readable",
                    column_name="display_name",
                ),
                Dimension(
                    name="description",
                    description="Brief summary or purpose of the collection",
                    column_name="description",
                ),
            ],
            primary_key="collection_id",
            measures=[
                Measure(
                    name="count",
                    description="The number of collections",
                    query="COUNT(self.collection_id)",
                ),
                Measure(
                    name="distinct_count",
                    description="The number of distinct collections",
                    query="COUNT(DISTINCT self.collection_id)",
                ),
            ],
        )
    )

    registry.register(
        Model(
            name="users",
            table=f"{catalog_name}.oso.users_v1",
            description=textwrap.dedent(
                """
                This model contains user profiles, including their unique identifiers, 
                source information, display names, profile pictures, bios, and URLs. 
                It is used to capture user identity across the OSO platform.
                """
            ),
            dimensions=[
                Dimension(
                    name="user_id",
                    description="The unique identifier for the user, as generated by OSO",
                    column_name="user_id",
                ),
                Dimension(
                    name="user_source_id",
                    description="The unique identifier for the user from the source",
                    column_name="user_source_id",
                ),
                Dimension(
                    name="user_source",
                    description="The source of the user (GITHUB, ENS, FARCASTER)",
                    column_name="user_source",
                ),
                Dimension(
                    name="display_name",
                    description="The display name of the user",
                    column_name="display_name",
                ),
                Dimension(
                    name="profile_picture_url",
                    description="The URL to the user profile picture",
                    column_name="profile_picture_url",
                ),
                Dimension(
                    name="bio",
                    description="A short biography or description of the user",
                    column_name="bio",
                ),
                Dimension(
                    name="url",
                    description="A URL to the user website",
                    column_name="url",
                ),
            ],
            primary_key="user_id",
            measures=[
                Measure(
                    name="count",
                    description="The number of users",
                    query="COUNT(self.user_id)",
                ),
                Measure(
                    name="distinct_count",
                    description="The number of distinct users",
                    query="COUNT(DISTINCT self.user_id)",
                ),
            ],
        )
    )

    registry.register(
        Model(
            name="contracts",
            table=f"{catalog_name}.oso.contracts_v0",
            description=textwrap.dedent(
                """
                This table contains information about smart contracts deployed across 
                various blockchain networks, including deployment details and relationships.
                """
            ),
            dimensions=[
                Dimension(
                    name="deployment_date",
                    description="The date of a contract deployment",
                    column_name="deployment_date",
                ),
                Dimension(
                    name="contract_address",
                    description="The address of the contract",
                    column_name="contract_address",
                ),
                Dimension(
                    name="contract_namespace",
                    description="The chain of the contract",
                    column_name="contract_namespace",
                ),
                Dimension(
                    name="originating_address",
                    description="The EOA address that initiated the contract deployment",
                    column_name="originating_address",
                ),
                Dimension(
                    name="factory_address",
                    description="The address of the factory that deployed the contract",
                    column_name="factory_address",
                ),
                Dimension(
                    name="root_deployer_address",
                    description="The EOA address that is considered the root deployer",
                    column_name="root_deployer_address",
                ),
                Dimension(
                    name="sort_weight",
                    description="A weight used for sorting contracts",
                    column_name="sort_weight",
                ),
            ],
            primary_key="contract_address",
            measures=[
                Measure(
                    name="count",
                    description="The number of contracts",
                    query="COUNT(self.contract_address)",
                ),
                Measure(
                    name="distinct_count",
                    description="The number of distinct contracts",
                    query="COUNT(DISTINCT self.contract_address)",
                ),
                Measure(
                    name="avg_sort_weight",
                    description="The average sort weight of contracts",
                    query="AVG(self.sort_weight)",
                ),
            ],
        )
    )

    registry.register(
        Model(
            name="repositories",
            table=f"{catalog_name}.oso.repositories_v0",
            description=textwrap.dedent(
                """
                This table contains information about source code repositories,
                primarily from GitHub, including repository metadata and statistics.
                """
            ),
            dimensions=[
                Dimension(
                    name="owner",
                    description="The owner of the repository",
                    column_name="owner",
                ),
                Dimension(
                    name="name",
                    description="The name of the repository",
                    column_name="name",
                ),
                Dimension(
                    name="url",
                    description="The URL of the repository",
                    column_name="url",
                ),
                Dimension(
                    name="is_fork",
                    description="Whether the repository is a fork",
                    column_name="is_fork",
                ),
                Dimension(
                    name="star_count",
                    description="The number of stars for the repository",
                    column_name="star_count",
                ),
                Dimension(
                    name="language",
                    description="The primary programming language of the repository",
                    column_name="language",
                ),
            ],
            primary_key=["owner", "name"],
            measures=[
                Measure(
                    name="count",
                    description="The number of repositories",
                    query="COUNT(*)",
                ),
                Measure(
                    name="total_stars",
                    description="The total number of stars across repositories",
                    query="SUM(self.star_count)",
                ),
                Measure(
                    name="avg_stars",
                    description="The average number of stars per repository",
                    query="AVG(self.star_count)",
                ),
            ],
        )
    )

    registry.register(
        Model(
            name="package_owners",
            table=f"{catalog_name}.oso.package_owners_v0",
            description=textwrap.dedent(
                """
                This table contains information about package owners across different
                package registries like NPM, PyPI, etc.
                """
            ),
            dimensions=[
                Dimension(
                    name="package_manager",
                    description="The package manager (NPM, PyPI, etc.)",
                    column_name="package_manager",
                ),
                Dimension(
                    name="package_name",
                    description="The name of the package",
                    column_name="package_name",
                ),
                Dimension(
                    name="owner_name",
                    description="The name of the package owner",
                    column_name="owner_name",
                ),
            ],
            primary_key=["package_manager", "package_name", "owner_name"],
            measures=[
                Measure(
                    name="count",
                    description="The number of package ownership records",
                    query="COUNT(*)",
                ),
            ],
        )
    )

    registry.register(
        Model(
            name="sboms",
            table=f"{catalog_name}.oso.sboms_v0",
            description=textwrap.dedent(
                """
                Software Bill of Materials (SBOM) data containing information about
                software dependencies and components.
                """
            ),
            dimensions=[
                Dimension(
                    name="sbom_type",
                    description="The type of SBOM",
                    column_name="sbom_type",
                ),
                Dimension(
                    name="component_name",
                    description="The name of the software component",
                    column_name="component_name",
                ),
                Dimension(
                    name="component_version",
                    description="The version of the software component",
                    column_name="component_version",
                ),
                Dimension(
                    name="license",
                    description="The license of the software component",
                    column_name="license",
                ),
            ],
            measures=[
                Measure(
                    name="count",
                    description="The number of SBOM entries",
                    query="COUNT(*)",
                ),
                Measure(
                    name="distinct_components",
                    description="The number of distinct components",
                    query="COUNT(DISTINCT self.component_name)",
                ),
            ],
        )
    )

    # ============================================"
    # RELATIONSHIP TABLES
    # ============================================"

    registry.register(
        Model(
            name="artifacts_by_project",
            table=f"{catalog_name}.oso.artifacts_by_project_v1",
            description=textwrap.dedent(
                """
                The join table between artifacts and projects. This table
                represents the many-to-many relationship between artifacts and
                projects.
                """
            ),
            dimensions=[
                Dimension(
                    name="artifact_id",
                    description="The unique identifier for the artifact",
                    column_name="artifact_id",
                ),
                Dimension(
                    name="project_id",
                    description="The unique identifier for the project",
                    column_name="project_id",
                ),
                Dimension(
                    name="artifact_source",
                    description="The original source of the artifact",
                    column_name="artifact_source",
                ),
                Dimension(
                    name="artifact_namespace",
                    description="The grouping or namespace of the artifact",
                    column_name="artifact_namespace",
                ),
                Dimension(
                    name="artifact_name",
                    description="The name of the artifact",
                    column_name="artifact_name",
                ),
                Dimension(
                    name="project_source",
                    description="The source of the project",
                    column_name="project_source",
                ),
                Dimension(
                    name="project_namespace",
                    description="The grouping or namespace of the project",
                    column_name="project_namespace",
                ),
                Dimension(
                    name="project_name",
                    description="The name of the project",
                    column_name="project_name",
                ),
            ],
            primary_key=["artifact_id", "project_id"],
            relationships=[
                Relationship(
                    source_foreign_key="project_id",
                    ref_model="projects",
                    ref_key="project_id",
                    type=RelationshipType.MANY_TO_ONE,
                ),
            ],
        )
    )

    registry.register(
        Model(
            name="projects_by_collection",
            table=f"{catalog_name}.oso.projects_by_collection_v1",
            description=textwrap.dedent(
                """
                The join table between projects and collections. This table
                represents the many-to-many relationship between projects and
                collections.
                """
            ),
            dimensions=[
                Dimension(
                    name="project_id",
                    description="The unique identifier of the project",
                    column_name="project_id",
                ),
                Dimension(
                    name="collection_id",
                    description="The unique identifier of the collection",
                    column_name="collection_id",
                ),
            ],
            primary_key=["project_id", "collection_id"],
            relationships=[
                Relationship(
                    source_foreign_key="collection_id",
                    ref_model="collections",
                    ref_key="collection_id",
                    type=RelationshipType.MANY_TO_ONE,
                ),
            ],
        )
    )

    registry.register(
        Model(
            name="artifacts_by_collection",
            table=f"{catalog_name}.oso.artifacts_by_collection_v1",
            description=textwrap.dedent(
                """
                The join table between artifacts and collections. This table represents 
                the many-to-many relationship between artifacts and collections.
                """
            ),
            dimensions=[
                Dimension(
                    name="artifact_id",
                    description="The unique identifier of the artifact",
                    column_name="artifact_id",
                ),
                Dimension(
                    name="collection_id",
                    description="The unique identifier of the collection",
                    column_name="collection_id",
                ),
            ],
            primary_key=["artifact_id", "collection_id"],
            relationships=[
                Relationship(
                    source_foreign_key="collection_id",
                    ref_model="collections",
                    ref_key="collection_id",
                    type=RelationshipType.MANY_TO_ONE,
                ),
            ],
        )
    )

    registry.register(
        Model(
            name="artifacts_by_user",
            table=f"{catalog_name}.oso.artifacts_by_user_v1",
            description=textwrap.dedent(
                """
                The join table between artifacts and users. This table represents 
                the many-to-many relationship between artifacts and users.
                """
            ),
            dimensions=[
                Dimension(
                    name="artifact_id",
                    description="The unique identifier of the artifact",
                    column_name="artifact_id",
                ),
                Dimension(
                    name="user_id",
                    description="The unique identifier of the user",
                    column_name="user_id",
                ),
            ],
            primary_key=["artifact_id", "user_id"],
            relationships=[
                Relationship(
                    source_foreign_key="user_id",
                    ref_model="users",
                    ref_key="user_id",
                    type=RelationshipType.MANY_TO_ONE,
                ),
            ],
        )
    )
