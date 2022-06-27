cd ymir && docker build -t industryessentials/ymir-backend:test --build-arg PIP_SOURCE=https://pypi.mirrors.ustc.edu.cn/simple --build-arg SERVER_MODE='dev' -f Dockerfile.backend .

cd web && docker build -t industryessentials/ymir-web:test --build-arg NPM_REGISTRY='https://registry.npm.taobao.org' .

cd ../..
docker-compose down -v && docker-compose up -d
