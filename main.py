import oci
import time

# Load the OCI configuration from the default location
config = oci.config.from_file()

# Create a DMS client
client = oci.database_migration.DatabaseMigrationClient(config)

# Define the source and target database connections
source_db_connection = oci.database_migration.models.CreateConnectionDetails(
    display_name='SourceDBConnection',
    database_type='ORACLE',
    hostname='source_hostname',
    username='source_username',
    password='source_password',
    sid='source_sid',
    port='source_port'
)

target_db_connection = oci.database_migration.models.CreateConnectionDetails(
    display_name='TargetDBConnection',
    database_type='AUTONOMOUS',
    hostname='target_hostname',
    username='target_username',
    password='target_password',
    sid='target_sid',
    port='target_port'
)

# Create a migration
create_migration_details = oci.database_migration.models.CreateMigrationDetails(
    display_name='MyMigration',
    source_connection_id='source_connection_id',
    target_connection_id='target_connection_id',
    type='ONLINE',
    migration_class='PREMIUM',
    exclude_objects=['schema.object1', 'schema.object2'],
    exclude_objects_from='SCHEMA',
    include_objects=['schema.object3', 'schema.object4'],
    include_objects_from='SCHEMA',
    database_link='db_link_name',
    network_config=oci.database_migration.models.CreateMigrationNetworkDetails(
        vcn_id='vcn_id',
        subnet_id='subnet_id',
        security_group_ids=['security_group_id']
    )
)

response = client.create_migration(create_migration_details)
migration_id = response.data.id
print(f"Migration ID: {migration_id}")

# Wait for the migration to complete
migration_status = ''
while migration_status != 'SUCCEEDED':
    migration = client.get_migration(migration_id)
    migration_status = migration.data.lifecycle_state
    print(f"Migration status: {migration_status}")
    if migration_status == 'FAILED':
        print("Migration failed.")
        break
    time.sleep(60)  # Wait for 1 minute before checking again

# Fetch the migration report
migration_report = client.get_migration_report(migration_id).data
report_url = migration_report.report_url
print(f"Migration report URL: {report_url}")
