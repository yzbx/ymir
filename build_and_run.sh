cd ymir && docker build -t industryessentials/ymir-backend:1.3.0 --build-arg PIP_SOURCE=https://pypi.mirrors.ustc.edu.cn/simple --build-arg SERVER_MODE='dev' -f Dockerfile.backend .

cd web && docker build -t industryessentials/ymir-web:1.3.0 --build-arg NPM_REGISTRY='https://registry.npm.taobao.org' .

cd ../..
docker-compose down -v && docker-compose up -d
