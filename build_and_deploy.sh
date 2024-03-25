# Lambda関数のビルド
cd terraform/modules/lambda/src
zip -r ./lambda_function.zip .
cd ../../../../

# Terraformを使ったデプロイ
cd terraform
terraform init
terraform apply -auto-approve
cd ..
