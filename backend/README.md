# Paparazzi backend service

This is the main backend server for the system. It exposes REST APIs for CRUD operations on all resources of the system.

It uses:

- `fastapi` - web framework
- `pynamodb` - dynamodb client
- `celery` - async message broker communication

## Development

This project uses `poetry` for dependency management.

Install dependencies

```bash
make install
```

Activate virtual environment

```bash
source venv/bin/activate
```

Start all services

```bash
make services
```

Start main server

```bash
make local.server
```


## Build from source

Backend server

```bash
make build.server
```

Worker

```bash
make build.worker
```

Beat (scheduler)

```bash
make build.beat
```

