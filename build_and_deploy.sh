# Lambda関数のビルド
cd lambda
zip -r ./lambda_function.zip .
zip -g lambda_function.zip lambda_function.py
cd ..

# Terraformを使ったデプロイ
cd terraform
terraform init
terraform apply -auto-approve
cd ..
