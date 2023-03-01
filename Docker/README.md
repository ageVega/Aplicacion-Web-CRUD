# Docker

## Construir imagen a partir de Dockerfile

```bash
docker build -t agevega/matrix:1.0 .
```

## Lanzar contenedor con nuestra aplicacion en funcionamiento

```bash
docker run -it --rm -d -p 8080:8080 --name matrix agevega/matrix:1.0
```

## Lanzar contenedor efímero para testing

```bash
docker run -it --rm -p 8080:8080 agevega/matrix:1.0 -c /bin/bash
```

## Entrar en un contenedor existente

```bash
docker exec -it container_name /bin/bash
```

