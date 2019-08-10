from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import datetime, date
from pytz import timezone
from bson.py3compat import string_type, PY3, text_type

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/users"
mongo = PyMongo(app)
#---------- rotas 


#---------- rota index OK

@app.route('/index')
def index():
    return render_template('index.html')


#---------- rota cadastrar OK

@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastrar.html')


@app.route('/cadastro', methods=['POST'])
def cadastro():
   
    if 'ContaInicial' in request.form and  'ContaFinal' in request.form and 'Valor' in request.form:
        date = datetime.now()
        fuso_horario = timezone('America/Sao_Paulo')
        data = date.astimezone(fuso_horario)
        mongo.db.users.insert({
            "ContaInicial" : request.form.get('ContaInicial'),
            "ContaFinal" : request.form.get('ContaFinal'),
            "Valor" : request.form.get('Valor'),
            "date_ano" :  data.year, "date_mes" :  data.month, 
            "date_dia" :  data.day, "date_hora" :  data.hour, "date_minuto" :  data.minute}) 
    return redirect(url_for('index'))
    

#---------- rota lista OK
@app.route('/lista')
def lista():
    userss = mongo.db.users.find()
    return render_template('lista.html', userss = userss)

#---------- rota deletar OK

@app.route('/deletar/<id>')
def deletar(id):
    transacao = mongo.db.users.delete_one({"_id": ObjectId(id)})
    userss = mongo.db.users.find()
    return render_template('lista.html', userss = userss)


#---------- rota atualizar OK
@app.route('/atualizar/<id>', methods=['GET','POST'])
def atualizar(id):
    print()
    if 'ContaInicial' in request.form and 'ContaFinal' in request.form and 'Valor' in request.form:
        ContaInicial = request.form.get('ContaInicial')
        ContaFinal = request.form.get('ContaFinal')
        Valor = request.form.get('Valor')
        mongo.db.users.update_one({'_id': ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)}, {'$set': {'ContaInicial': ContaInicial, 'ContaFinal': ContaFinal, 'Valor': Valor}})
        userss = mongo.db.users.find({"_id": ObjectId(id)})
        return redirect(url_for('lista'))
    userss = mongo.db.users.find({"_id": ObjectId(id)})[0]
    return render_template('atualizar.html', userss = userss)
      



#---------- rota  filtrar OK

@app.route('/filtrar')
def filtrar():
    return render_template('filtrar.html')

@app.route('/filtro', methods=['POST'])
def filtro():
    if 'Date' in request.form and 'Valor' in request.form and 'Hora' in request.form:
        date = request.form.get('Date')
        valor = request.form.get('Valor')
        hora = request.form.get('Hora')
        data_ano = int(date[:4])
        data_mes = int(date[5:7])
        data_dia = int(date[8:10])#por seguranca
        data_mes = int(date[5:7])
        time_hora = int(hora[0:2])
        time_min = int(hora[3:5])
        
        userss = mongo.db.users.find({'Valor':{'$gte': valor},'date_ano' :{'$gte': data_ano}, 'date_mes' :{'$gte': data_mes},
        'date_dia' :{'$gte': data_dia},'date_hora' :{'$gte': time_hora}, 'date_minuto' :{'$gte': time_min},  })
        transacao = dumps(userss)   
    return transacao
    #return render_template('lista2.html', transacaos = listatransacaos) # ajeitar o render!!!


#---------- main / run
if __name__ == '__main__':
    app.run(debug=True)
