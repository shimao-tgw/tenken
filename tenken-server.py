from tenkenapp import create_app

app = create_app()
app.secret_key ="0195255551"

if __name__ == '__main__':

     
     # '0.0.0.0'を指定してすべてのIPからアクセス可能に
     app.run(host="0.0.0.0", port=5000)
