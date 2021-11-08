# Laravel Memo
[Laravel入門 - 使い方チュートリアル - - Qiita](https://qiita.com/sano1202/items/6021856b70e4f8d3dc3d)
## Install
requirements:
&emsp;**PHP(over 7.2ver)**
&emsp;**conposer 2.XX**
&emsp;**artisan**

## Create project
>composer create-project laravel/laravel sample

## ルーティング定義
php artisan route:list

## DB
.env
>DB_CONNECTION=mysql 
>DB_HOST=127.0.0.1 
>DB_PORT=3306 
>DB_DATABASE=db_name 
>DB_USERNAME=db_name 
>DB_PASSWORD=db_pw

## Migration
Roll back
>php artisan migrate:reset
>php artisan migrate

PHP
>Schema::dropIfExists('table_name');

integer
>$table->integer('phone_number')->length(20);

小数を扱うカラム
>$table->float('column1',  8,  2);

## Model
>php artisan make:model model_name

## Run server
>php artisan serve --host=localhost --port=8000

## Seed
DBのテストデータ挿入
>php artisan db:seed

## 再マイグレーション＆seed実行
>php artisan migrate:refresh --seed

## フォームから書いた内容をDBに書き込む
>[【Laravel】フォームから書いた内容をDBに書き込む方法 - SEブログ (soma-engineering.com)](https://soma-engineering.com/coding/php/form-store-db/2018/06/21/)

## DBの内容をブラウザに表示する
>[【Laravel】DBの内容をブラウザに表示する方法 - SEブログ (soma-engineering.com)](https://soma-engineering.com/coding/php/display-contents-view/2018/06/18/)


