# SAMS Settings: Environment Variables
## Base Settings:
* **SAMS_MONGO_URI**: Defaults to 'mongodb://localhost/sams'
* **SAMS_ELASTICSEARCH_URL**: Defaults to 'http://localhost:9200'
* **SAMS_ELASTICSEARCH_INDEX**: Defaults to: 'sams'
* **SAMS_PUBLIC_URL**: Defaults to 'http://localhost:5750' (Must be the public URL from Cloudflare, for Fidelities website to SAMS public files)

## Storage Destination(s):

### Example Mongo GridFS Storage
**STORAGE_DESTINATION_1**='MongoGridFS,files,mongodb://localhost/sams_files'
* **Provider**: MongoGridFS
* **Name**: files
* **Mongo URI**: mongodb://localhost/sams_files

### Example Amazon S3 Storage
**STORAGE_DESTINATION_1**='AmazonS3Provider,files,access=access123,secret=secret456,region=eu-west-3,bucket=sams_files'
* **Provider**: AmazonS3Provider
* **Name**: files
* **Access Key**: access123
* **Secret Key**: secret456
* **Region**: eu-west-3
* **Bucket**: sams_files

## API:
* **SAMS_API_HOST**: Defaults to 'localhost'
* **SAMS_API_PORT**: Defaults to '5700'
* **SAMS_API_URL**: Defaults to 'http://localhost:5700'
* **SAMS_API_WORKERS**: Defaults to (cpu_count + 1)
* **SAMS_API_TIMEOUT**: Defaults to '30'
* **SAMS_API_AUTH**: Defaults to 'sams.auth.public'
* **SAMS_MAX_ASSET_SIZE**: Defaults to '0' - unlimited

## Public File Server:
* **SAMS_PUBLIC_HOST**: Defaults to '0.0.0.0'
* **SAMS_PUBLIC_PORT**: Defaults to '5750'
* **SAMS_API_URL**: Defaults to 'http://0.0.0.0:5750'
* **SAMS_PUBLIC_WORKERS**: Defaults to (cpu count + 1)
* **SAMS_PUBLIC_TIMEOUT**: Defaults to '30'
* **SAMS_PUBLIC_AUTH**: Defaults to 'sams.auth.public'
