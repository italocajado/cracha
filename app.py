
from flask import Flask, render_template, request, redirect, url_for
from reportlab.pdfgen import canvas
from io import BytesIO

app = Flask(__name__)

# Dicionário para armazenar os dados dos funcionários
funcionarios = []

@app.route('/')
def index():
    return render_template('index.html', funcionarios=funcionarios)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome_preferido = request.form.get('nome_preferido')
    setor = request.form.get('setor')
    terceirizado = request.form.get('terceirizado')
    nome_completo = request.form.get('nome_completo')
    cpf = request.form.get('cpf')
    matricula = request.form.get('matricula')

    funcionario = {
        'nome_preferido': nome_preferido,
        'setor': setor,
        'terceirizado': terceirizado,
        'nome_completo': nome_completo,
        'cpf': cpf,
        'matricula': matricula
    }

    funcionarios.append(funcionario)
    return redirect('/')

@app.route('/gerar_cracha/<int:funcionario_id>')
def gerar_cracha(funcionario_id):
    funcionario = funcionarios[funcionario_id]
    output = BytesIO()
    p = canvas.Canvas(output)

    # Lado da frente do crachá
    p.drawString(100, 750, f"Nome Preferido: {funcionario['nome_preferido']}")
    p.drawString(100, 730, f"Setor: {funcionario['setor']}")
    p.drawString(100, 710, f"Terceirizado: {funcionario['terceirizado']}")
    
    # Lado de trás do crachá
    p.drawString(100, 350, f"Nome Completo: {funcionario['nome_completo']}")
    p.drawString(100, 330, f"CPF: {funcionario['cpf']}")
    p.drawString(100, 310, f"Matrícula: {funcionario['matricula']}")

    p.showPage()
    p.save()

    output.seek(0)
    return output.read(), 200, {'Content-Type': 'application/pdf'}

if __name__ == '__main__':
    app.run(debug=True)
