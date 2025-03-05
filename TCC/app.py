#? Importação de bibliotecas.
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
import mysql.connector  

#? Configuração do Flask.
app = Flask(__name__)

#? Conecta ao Banco de Dados    
app.config['SECRET_KEY'] = 'root'  # Chave secreta
def conectar_banco():
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password="", 
        database='estoque_laboratorio_db',
        port = 3306
    )
    return cnx

#? ROTAS PARA OS TEMPLATES
#! Rotas relacionadas ao LOGIN e CADASTRO
@app.route('/')
def inicio():
    return render_template('login.html')

@app.route('/cadastro_usuario')
def cadastro_usuario():
    return render_template('cadastro.html')

@app.route('/recupera_senha')
def recupera_senha():
    return render_template('recupera_senha.html')

@app.route('/nova_senha')
def nova_senha():
    return render_template('nova_senha.html')

#! Rotas relacionadas ao ESTOQUE
@app.route('/estoque')
def estoque():
    return render_template('estoque.html')

@app.route('/criar_estoque')
def criar_estoque():
    return render_template('criar_estoque.html')

@app.route('/mudar_estoque')
def mudar_estoque():
    return render_template('mudar_estoque.html')

#! Rotas relacionadas ao EXAME
@app.route('/exame')
def exame():
    return render_template('exame.html')

@app.route('/criar_exame')
def criar_exame():
    return render_template('criar_exame.html')

@app.route('/mudar_exame')
def mudar_exame():
    return render_template('mudar_exame.html')

@app.route('/criar_exame2')
def criar_exame2():
    return render_template('criar_exame2.html')


#! Rotas relacionadas ao PACIENTE
@app.route('/paciente')
def paciente():
    return render_template('paciente.html')

@app.route('/criar_paciente')
def criar_paciente():
    return render_template('criar_paciente.html')

@app.route('/mudar_paciente')
def mudar_paciente():
    return render_template('mudar_paciente.html')

#! Rotas relacionadas ao DESPESAS
@app.route('/despesa')
def despesa():
    return render_template('despesa.html')

@app.route('/criar_despesa')
def criar_despesa():
    return render_template('criar_despesa.html')

@app.route('/mudar_despesa')
def mudar_despesa():
    return render_template('mudar_despesa.html')

#! Rotas relacionadas ao USUARIOS
@app.route('/usuario')
def usuario():
    if session.get('user_id') != 1: 
        flash('Acesso negado: você não tem permissão para acessar esta página.', 'danger')
        return redirect('/tela_inicial') 
    return render_template('usuario.html')

@app.route('/mudar_usuario')
def mudar_usuario():
    return render_template('mudar_usuario.html')

#! Rota para o LOGOUT do usuário.
@app.route('/logout', methods=['POST'])
def logout():
    # Aqui você pode limpar informações de sessão ou cookies se estiver utilizando
    flash('Você foi deslogado com sucesso!', 'info')
    return render_template('login.html')

#! Rota para o CONTROLE DE DATA.
@app.template_filter('to_datetime')
def to_datetime_filter(date_value, format='%Y-%m-%d'):
    # Verificar se date_value é uma string ou já é um objeto datetime
    if isinstance(date_value, str):
        # Se for string, convertemos para datetime
        return datetime.strptime(date_value, format).date()
    elif isinstance(date_value, datetime):
        # Se for datetime, retornamos apenas a parte da data (sem a hora)
        return date_value.date()
    return date_value  # Retorna o valor original se não for string ou datetime













# Função para buscar o código de acesso atual do banco de dados
def obter_codigo_acesso():
    connection = conectar_banco()
    cursor = connection.cursor()
    cursor.execute("SELECT codigo_acesso FROM configuracoes ORDER BY id DESC LIMIT 1;")
    codigo_acesso = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return codigo_acesso

# Função para atualizar o código de acesso no banco de dados
def atualizar_codigo_acesso(novo_codigo):
    connection = conectar_banco()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO configuracoes (codigo_acesso) VALUES (%s);", (novo_codigo,))
    connection.commit()
    cursor.close()
    connection.close()

# Rota para alterar o código de acesso globalmente
@app.route('/mudar_codigo_acesso_global', methods=['POST'])
def mudar_codigo_acesso_global():
    if request.method == 'POST':
        novo_codigo = request.form['novo_codigo']
        if novo_codigo:
            try:
                atualizar_codigo_acesso(novo_codigo)
                flash("Código de acesso alterado com sucesso!", "success")
            except Exception as e:
                flash(f"Erro ao atualizar o código de acesso: {str(e)}", "error")
    return redirect(url_for('usuario'))

# Rota de cadastro com código de acesso dinâmico
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    mensagem_erro = None  # Inicializa a variável de mensagem de erro como None

    if request.method == 'POST':
        # Recebe os dados do formulário via POST
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        telefone = request.form['telefone']
        cpf = request.form['cpf']
        cidade = request.form['cidade']
        nome_mae = request.form['nome_mae']
        nome_professor = request.form['nome_professor']
        aceso = request.form['aceso']  # Código de acesso inserido pelo usuário

        # Obtém o código de acesso atual do banco de dados
        acesso_atual = obter_codigo_acesso()

        # Verifica se o código de acesso está correto
        if acesso_atual != aceso:
            mensagem_erro = 'Código de acesso incorreto!'
        else:
            # Verifica se o email já existe no banco (considerando inativo)
            connection = conectar_banco()
            cursor = connection.cursor()

            cursor.execute("SELECT id, ativo FROM usuarios WHERE email = %s", (email,))
            usuario_existente = cursor.fetchone()

            if usuario_existente:
                # Se o usuário existir e estiver inativo, reativa
                if usuario_existente[1] == 0:  # Se estiver inativo
                    cursor.execute("UPDATE usuarios SET ativo = 1 WHERE email = %s", (email,))
                    connection.commit()
                    flash('Usuário reativado com sucesso!', 'success')
                else:
                    flash('Email já cadastrado e ativo.', 'error')
            else:
                # Caso o email não exista, cria um novo usuário
                try:
                    SQL = "INSERT INTO usuarios (nome, email, senha, telefone, cpf, cidade, nome_mae, nome_professor, ativo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1);"
                    values = (nome, email, senha, telefone, cpf, cidade, nome_mae, nome_professor)
                    cursor.execute(SQL, values)
                    connection.commit()
                    flash('Cadastro efetuado com sucesso!', 'success')
                except Exception as e:
                    flash(f"Erro ao cadastrar usuário: {str(e)}", 'error')

            cursor.close()
            connection.close()

            # Redireciona para a página inicial após cadastro ou reativação
            return redirect(url_for('inicio'))

    return render_template('cadastro.html', mensagem_erro=mensagem_erro)



# Rota para o LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        # Conectar ao banco de dados
        cnx = conectar_banco()
        cursor = cnx.cursor()

        # Buscar o usuário pelo email
        cursor.execute("""
            SELECT id, nome, email, senha 
            FROM usuarios 
            WHERE email = %s;
        """, (email,))

        user = cursor.fetchone()

        cursor.close()
        cnx.close()

        if user:
            print(f"Usuário encontrado: {user}")
            # A comparação simples de senha
            if user[3] == senha:  # Comparando a senha diretamente (sem hash)
                # Se a senha for correta, armazena o id do usuário na sessão
                session['user_id'] = user[0]
                session['user_name'] = user[1]
                session['user_email'] = user[2]
                return redirect(url_for('tela_inicial'))
            else:
                flash('Senha incorreta.', 'error')
        else:
            flash('Email não encontrado.', 'error')

    return render_template('login.html')

#? Rota para o RECUPERA SENHA do website.
@app.route('/recupera', methods=['POST'])
def recupera():
    cidade = request.form.get('cidade')
    nome_mae = request.form.get('nome_mae')
    nome_professor = request.form.get('nome_professor')

    cnx = conectar_banco()
    cursor = cnx.cursor()

    query = "SELECT * FROM usuarios WHERE cidade = %s AND nome_mae = %s AND nome_professor = %s;"
    values = (cidade, nome_mae, nome_professor)
    cursor.execute(query, values)

    user = cursor.fetchone()

    cursor.close()
    cnx.close()

    if user:
        return redirect(url_for('nova_senha'))
    else:
        mensagem_erro = 'Alguma informação está incorreta'
        return render_template('recupera_senha.html', mensagem_erro=mensagem_erro)

#? Rota para o TROCAR SENHA do website.
@app.route('/troca_senha', methods=['GET', 'POST'])
def troca_senha():
    if request.method == 'POST':
        cpf = request.form.get('cpf')
        nova_senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')

        # Verifica se a nova senha e a confirmação são iguais
        if nova_senha != confirmar_senha:
            mensagem_erro = 'As senhas não coincidem. Tente novamente.'
            return render_template('nova_senha.html', mensagem_erro=mensagem_erro)
        
        # Verifica se o email está cadastrado
        cnx = conectar_banco()
        cursor = cnx.cursor()

        query = "SELECT * FROM usuarios WHERE cpf = %s;"
        values = (cpf,)
        cursor.execute(query, values)

        user = cursor.fetchone()

        if not user:
            cursor.close()
            cnx.close()
            mensagem_erro = 'Este cpf não está cadastrado.'
            return render_template('nova_senha.html', mensagem_erro=mensagem_erro)
        
        # Atualiza a senha no banco de dados
        query = "UPDATE usuarios SET senha = %s WHERE cpf = %s;"
        values = (nova_senha, cpf)
        cursor.execute(query, values)
        cnx.commit()

        cursor.close()                                  
        cnx.close()

        return redirect(url_for('inicio'))

    return render_template('nova_senha.html')










#? Rota para o AVISO DE ESTOQUE do website.
# Rota para a tela inicial (aviso de estoque) - Todos os usuários têm acesso
# Rota para a tela inicial
@app.route('/tela_inicial')
def tela_inicial():
    # Se o usuário não estiver logado, redireciona para o login
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Listas para produtos vencidos ou prestes a vencer
    produtos_vencendo_3 = []  # Produtos com vencimento em até 3 meses
    produtos_vencendo_6 = []  # Produtos com vencimento em até 6 meses
    produtos_vencidos = []    # Produtos já vencidos

    # Conectar ao banco de dados
    cnx = conectar_banco()
    cursor = cnx.cursor()

    # Buscar produtos com validade
    cursor.execute("""
        SELECT produto, validade 
        FROM estoque 
        WHERE ativo = 1;
    """)

    produtos = cursor.fetchall()

    hoje = datetime.now().date()  # Data atual

    for produto, validade in produtos:
        if isinstance(validade, datetime):
            validade = validade.date()  # Converte para datetime.date se for datetime.datetime

        # Verifica a situação do produto com base na validade
        if validade < hoje:  # Produto vencido
            produtos_vencidos.append(produto)
        elif validade <= hoje + timedelta(days=90):  # 3 meses ou menos
            produtos_vencendo_3.append(produto)
        elif validade <= hoje + timedelta(days=180):  # 6 meses ou menos
            produtos_vencendo_6.append(produto)

    cursor.close()
    cnx.close()

    # Mensagem de alerta com produtos
    mensagem_alerta = ""
    
    if produtos_vencidos:
        mensagem_alerta += f"<strong style='color: red;'>Produtos vencidos:</strong> " + ', '.join(produtos_vencidos)
    
    if produtos_vencendo_3:
        if mensagem_alerta:
            mensagem_alerta += "<br>"
        mensagem_alerta += f"<strong style='color: black;'>Produtos próximos do vencimento (3 meses):</strong> " + ', '.join(produtos_vencendo_3)
    
    if produtos_vencendo_6:
        if mensagem_alerta:
            mensagem_alerta += "<br>"
        mensagem_alerta += f"<strong style='color: black;'>Produtos próximos do vencimento (6 meses):</strong> " + ', '.join(produtos_vencendo_6)

    # Passa a mensagem de alerta para o template
    return render_template('tela_inicial.html', mensagem_erro=mensagem_alerta)










#? Rota para o EXIBE ESTOQUE
@app.route('/exibe_estoque')
def exibe_estoque():
    connection = conectar_banco()
    cursor = connection.cursor()
    estoque_com_validade = []
    
    try:
        # Alteração aqui: consulta agora ordena pelo campo 'validade' de forma crescente
        cursor.execute("SELECT * FROM estoque WHERE ativo = 1 ORDER BY validade ASC")
        dados_estoque = cursor.fetchall()
        
        for item in dados_estoque:
            validade = item[6]  # Índice da data de validade
            # Se validade for string, converta para data
            if isinstance(validade, str):
                validade = datetime.strptime(validade, '%Y-%m-%d').date()
            
            # Se validade já for datetime ou date, compare com a data atual
            item_valido = validade >= datetime.now().date()

            # Definir o limite de proximidade para validade (7 dias antes da data de validade)
            proximidade_validade = datetime.now().date() <= validade <= datetime.now().date() + timedelta(days=90)

            # Definir a classe CSS para a validade
            validade_class = 'table-warning' if proximidade_validade else ''
            validade_class = 'table-danger' if not item_valido else validade_class

            estoque_com_validade.append({
                'id': item[0],
                'produto': item[1],
                'categoria': item[2],
                'chegada': item[3],
                'teste': item[4],
                'lote': item[5],
                'validade': validade,
                'estoque_final': item[7],
                'valido': item_valido,
                'validade_class': validade_class  # Passando a classe para o template
            })

    except Exception as e:
        flash(f"Erro ao acessar o banco de dados: {str(e)}", 'error')
        print(f"Erro ao acessar o banco de dados: {e}")
    
    finally:
        cursor.close()
        connection.close()

    return render_template('estoque.html', dados_estoque=estoque_com_validade)

#? Rota para o CRIAR ESTOQUE
@app.route('/cria_estoque', methods=['GET', 'POST'])
def cria_estoque():
    if request.method == 'POST':
        # Pegando os dados do formulário
        produto = request.form['produto']
        categoria = request.form['categoria']
        chegada = request.form['chegada']
        teste = request.form['teste']
        lote = request.form['lote']
        validade = request.form['validade']
        estoque_final = request.form['estoque_final']
        obs = request.form['obs']

        # Inserir dados no banco de dados
        connection = conectar_banco()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO estoque (produto, categoria, chegada, teste, lote, validade, estoque_final, obs) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
            (produto, categoria, chegada, teste, lote, validade, estoque_final, obs)
        )
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('exibe_estoque'))
    else:
        return render_template('criar_estoque.html')

#? Rota para o EDITAR ESTOQUE
@app.route('/editar_estoque', methods=['POST'])
@app.route('/editar_estoque/<id>', methods=['GET', 'POST'])
def editar_estoque(id=None):
    print(f"Requested ID: {id}")
    print(f"Request method: {request.method}")

    # Verifica se o método de requisição é POST ou GET.
    if request.method == 'POST':
        # Recebe os dados do formulário via POST.
        id = request.form['id']  # Este ID deve ser o ID do estoque que você está editando.
        produto = request.form['produto']  # Campo correto
        categoria = request.form['categoria']  # Campo correto
        chegada = request.form['chegada']
        teste = request.form['teste']
        lote = request.form['lote']
        validade = request.form['validade']
        estoque_final = request.form['estoque_final']
        obs = request.form['obs']
        
        # Faz a conexão com o banco de dados.
        connection = conectar_banco()
        cursor = connection.cursor()

        # Monta a instrução SQL para atualização dos dados do estoque.
        SQL = """UPDATE estoque 
                 SET produto = %s, categoria = %s, chegada = %s, teste = %s, 
                     lote = %s, validade = %s, estoque_final = %s, obs = %s 
                 WHERE id = %s;"""
        
        values = (produto, categoria, chegada, teste, lote, validade, estoque_final, obs, id)
        cursor.execute(SQL, values)
        connection.commit()

        # Fecha a conexão com o banco de dados.
        cursor.close()
        connection.close()

        # Redireciona para a tela de estoque novamente.
        return redirect(url_for('exibe_estoque'))
    else:
        # Faz a conexão com o banco de dados para obter os dados do estoque.
        connection = conectar_banco()
        cursor = connection.cursor()

        # Monta a instrução SQL para trazer os dados do estoque.
        SQL = "SELECT * FROM estoque WHERE id = %s;"
        cursor.execute(SQL, (id,))
        estoque = cursor.fetchone()

        # Fecha a conexão com o banco de dados.
        cursor.close()
        connection.close()

        # Redireciona para a tela de edição de estoque.
        return render_template('mudar_estoque.html', estoque=estoque)
    
#? Rota para o DESCONTAR ESTOQUE
@app.route('/descontar_estoque/<int:id>', methods=['POST'])
def descontar_estoque(id):
    try:
        # Conexão com o banco de dados
        connection = conectar_banco()
        cursor = connection.cursor()

        # Obtém os reagentes e as quantidades necessárias para o exame
        cursor.execute(
            """SELECT fitc, quantidade1, pe, quantidade2, 
                      ecd, quantidade3, pc55, quantidade4, 
                      pc7, quantidade5, apc, quantidade6, 
                      a700, quantidade7, a750, quantidade8, pb, quantidade9, ko, quantidade10 
              FROM exames WHERE id = %s;""", (id,)
        )
        exame = cursor.fetchone()

        if exame:
            # Coleta as quantidades do exame
            fitc, quantidade1, pe, quantidade2, ecd, quantidade3, pc55, quantidade4, pc7, quantidade5, apc, quantidade6, a700, quantidade7, a750, quantidade8, pb, quantidade9, ko, quantidade10 = exame
            quantidades = [quantidade1, quantidade2, quantidade3, quantidade4, quantidade5, quantidade6, quantidade7, quantidade8, quantidade9, quantidade10]
            reagentes = [fitc, pe, ecd, pc55, pc7, apc, a700, a750, pb, ko]  # Reagentes correspondentes

            erro_estoque = False  # Flag para erro de estoque insuficiente
            itens_vencidos = []  # Lista para armazenar itens fora de validade
            itens_faltando = []  # Lista para armazenar os itens que faltam no estoque

            # Loop para verificar o estoque de cada reagente
            for idx in range(len(quantidades)):
                if quantidades[idx] > 0:
                    nome_produto = reagentes[idx]

                    # Verifica o estoque atual pelo nome do produto, ordenando pela validade mais próxima
                    cursor.execute(
                        """SELECT id, estoque_final, validade FROM estoque 
                           WHERE produto = %s AND ativo = 1 
                           ORDER BY validade ASC;""", (nome_produto,)
                    )
                    estoques = cursor.fetchall()

                    if estoques:
                        estoque_final = 0
                        validade_mais_proxima = None
                        item_a_descontar = None

                        # Procurar o item mais próximo da validade
                        for item in estoques:
                            item_id, estoque_final_item, validade = item

                            # Se o produto ainda está dentro da validade
                            if validade >= datetime.now().date():
                                if validade_mais_proxima is None or validade < validade_mais_proxima:
                                    validade_mais_proxima = validade
                                    estoque_final = estoque_final_item
                                    item_a_descontar = item_id

                        if item_a_descontar:
                            # Verifica se há estoque suficiente para descontar
                            if estoque_final >= quantidades[idx]:
                                # Desconta o estoque do item com a validade mais próxima
                                novo_estoque = estoque_final - quantidades[idx]
                                cursor.execute(
                                    "UPDATE estoque SET estoque_final = %s WHERE id = %s;", (novo_estoque, item_a_descontar)
                                )
                            else:
                                erro_estoque = True
                                break  # Interrompe se o estoque não for suficiente
                        else:
                            # Se não houver um item válido para descontar
                            itens_vencidos.append(nome_produto)

                    else:
                        # Se o produto não estiver no estoque, adiciona à lista de itens faltando
                        itens_faltando.append(nome_produto)

            # Commit para salvar as alterações, se não houver erros
            if not erro_estoque and not itens_vencidos and not itens_faltando:
                connection.commit()

            # Flash de erro de validade, estoque insuficiente ou itens faltando
            if itens_vencidos:
                flash(f"Não é possível descontar do estoque pois os seguintes itens estão vencidos: {', '.join(itens_vencidos)}", "danger")
            elif erro_estoque:
                flash("Estoque insuficiente para descontar os reagentes necessários para o exame.", "danger")
            elif itens_faltando:
                flash(f"Os seguintes itens não estão no estoque: {', '.join(itens_faltando)}", "danger")
            else:
                flash("Estoque descontado com sucesso.", "success")

    except Exception as e:
        print(f"Erro ao descontar estoque: {str(e)}")
        flash(f"Erro ao processar a operação: {str(e)}", "danger")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('exibe_exame'))  # Redireciona para a lista de exames
    
#? Rota para o EXCLUIR ESTOQUE
@app.route('/excluir_estoque/<id>')
def excluir_estoque(id):

    # Faz a conexão com o banco de dados.
    connection = conectar_banco()
    cursor = connection.cursor()

    # Monta a instrução SQL para excluir logicamente o livro.
    SQL = "UPDATE estoque SET ativo = 0 WHERE id = %s;"
    cursor.execute(SQL, (id,))
    connection.commit()

    # Fecha a conexão com o banco de dados.
    cursor.close()
    connection.close()

    # Redireciona para a tela de listagem de livros.
    return redirect(url_for('exibe_estoque'))

#? Rota para DETALHAR ESTOQUE
@app.route('/detalhar_estoque/<int:id>')
def detalhar_estoque(id):
    cnx = conectar_banco()
    cursor = cnx.cursor()

    # Consulta para obter os detalhes do estoque
    query = "SELECT * FROM estoque WHERE id = %s"
    cursor.execute(query, (id,))
    estoque = cursor.fetchone()

    if not estoque:
        flash('Estoque não encontrado.', 'danger')
        return redirect(url_for('exibe_estoque'))

    # Busca exames associados ao estoque
    cursor.execute("SELECT nome_exame FROM exames WHERE id = %s", (estoque[2],))
    exame = cursor.fetchone()

    cursor.close()
    cnx.close()
    return render_template('detalhar_estoque.html', estoque=estoque, exame=exame)

    







    
#? Rota para o EXIBE EXAME
@app.route('/exibe_exame')
def exibe_exame():
    cnx = conectar_banco()
    cursor = cnx.cursor()

    query = """
    SELECT exames.id, exames.nome_exame
    FROM exames 
    WHERE exames.ativo = 1
    """

    cursor.execute(query)
    dados_exame = cursor.fetchall()

    cursor.close()
    cnx.close()

    return render_template('exame.html', dados_exame=dados_exame)

#? Rota para o CRIAR EXAME
@app.route('/cria_exame', methods=['GET', 'POST'])
def cria_exame():
    if request.method == 'POST':
        nome_exame = request.form['nome_exame']
        fitc = request.form['fitc']
        quantidade1 = request.form['quantidade1']
        pe = request.form['pe']
        quantidade2 = request.form['quantidade2']
        ecd = request.form['ecd']
        quantidade3 = request.form['quantidade3']
        pc5_5 = request.form['pc5.5']
        quantidade4 = request.form['quantidade4']
        pc7 = request.form['pc7']
        quantidade5 = request.form['quantidade5']
        apc = request.form['apc']
        quantidade6 = request.form['quantidade6']
        a700 = request.form['a700']
        quantidade7 = request.form['quantidade7']
        a750 = request.form['a750']
        quantidade8 = request.form['quantidade8']
        pb = request.form['pb']
        quantidade9 = request.form['quantidade9']
        ko = request.form['ko']
        quantidade10 = request.form['quantidade10']
        dupli_pe = request.form['dupli_pe']
        dupli1 = request.form['dupli1']
        dupli_a750 = request.form['dupli_a750']
        dupli2 = request.form['dupli2']
        dupli_pb = request.form['dupli_pb']
        dupli3 = request.form['dupli3']
        

        # Inserir o novo exame no banco de dados
        connection = conectar_banco()
        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO exames (nome_exame, fitc, quantidade1, pe, quantidade2, 
                                   ecd, quantidade3, pc55, quantidade4, pc7, 
                                   quantidade5, apc, quantidade6, a700, 
                                   quantidade7, a750, quantidade8, pb, 
                                   quantidade9, ko, quantidade10, dupli_pe, 
                                   dupli1, dupli_a750, dupli2, dupli_pb, dupli3) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s)""",
            (nome_exame, fitc, quantidade1, pe, quantidade2, 
             ecd, quantidade3, pc5_5, quantidade4, pc7, 
             quantidade5, apc, quantidade6, a700, 
             quantidade7, a750, quantidade8, pb, 
             quantidade9, ko, quantidade10, dupli_pe, 
             dupli1, dupli_a750, dupli2, dupli_pb, dupli3)
        )
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('exibe_exame'))
    else:
        return render_template('criar_exame.html')  # Adicione a lógica para mostrar o formulário aqui

#? Rota para o EDITAR EXAME
@app.route('/editar_exame/<int:id>', methods=['GET', 'POST'])
def editar_exame(id):
    cnx = conectar_banco()
    cursor = cnx.cursor()

    if request.method == 'POST':
        # Recebe os dados do formulário via POST
        nome_exame = request.form['nome_exame']
        fitc = request.form['fitc']
        quantidade1 = request.form['quantidade1']
        pe = request.form['pe']
        quantidade2 = request.form['quantidade2']
        ecd = request.form['ecd']
        quantidade3 = request.form['quantidade3']
        pc55 = request.form['pc55']
        quantidade4 = request.form['quantidade4']
        pc7 = request.form['pc7']
        quantidade5 = request.form['quantidade5']
        apc = request.form['apc']
        quantidade6 = request.form['quantidade6']
        a700 = request.form['a700']
        quantidade7 = request.form['quantidade7']
        a750 = request.form['a750']
        quantidade8 = request.form['quantidade8']
        pb = request.form['pb']
        quantidade9 = request.form['quantidade9']
        ko = request.form['ko']
        quantidade10 = request.form['quantidade10']
        dupli_pe = request.form['dupli_pe']
        dupli1 = request.form['dupli1']
        dupli_a750 = request.form['dupli_a750']
        dupli2 = request.form['dupli2']
        dupli_pb = request.form['dupli_pb']
        dupli3 = request.form['dupli3']

        # Atualiza os dados do exame no banco de dados
        query = """
        UPDATE exames SET nome_exame = %s, fitc = %s, quantidade1 = %s, pe = %s, quantidade2 = %s,
                          ecd = %s, quantidade3 = %s, pc55 = %s, quantidade4 = %s, pc7 = %s,
                          quantidade5 = %s, apc = %s, quantidade6 = %s, a700 = %s,
                          quantidade7 = %s, a750 = %s, quantidade8 = %s, pb = %s,
                          quantidade9 = %s, ko = %s, quantidade10 = %s, dupli_pe = %s, 
                          dupli1 = %s, dupli_a750 = %s, dupli2 = %s, dupli_pb = %s, dupli3 = %s
        WHERE id = %s
        """
        values = (nome_exame, fitc, quantidade1, pe, quantidade2, ecd, quantidade3, pc55,
                  quantidade4, pc7, quantidade5, apc, quantidade6, a700, quantidade7,
                  a750, quantidade8, pb, quantidade9, ko, quantidade10, dupli_pe, 
                  dupli1, dupli_a750, dupli2, dupli_pb, dupli3, id)
        
        cursor.execute(query, values)
        cnx.commit()
        

        cursor.close()
        cnx.close()

        return redirect(url_for('exibe_exame'))
    else:
        # Se for um GET, busca os dados do exame para preencher o formulário
        cursor.execute("SELECT * FROM exames WHERE id = %s", (id,))
        exame = cursor.fetchone()
        cursor.close()
        cnx.close()
        
        return render_template('mudar_exame.html', exame=exame)


#? Rota para o EXCLUIR EXAME
@app.route('/excluir_exame/<int:id>', methods=['GET'])
def excluir_exame(id):
    cnx = conectar_banco()
    cursor = cnx.cursor()

    # Marca o exame como inativo (exclusão lógica)
    query = "UPDATE exames SET ativo = 0 WHERE id = %s"
    cursor.execute(query, (id,))
    cnx.commit()

    cursor.close()
    cnx.close()

    return redirect(url_for('exibe_exame'))

#? Rota para DETALHAR EXAME
@app.route('/detalhar_exame/<int:id>', methods=['GET'])
def detalhar_exame(id):
    cnx = conectar_banco()
    cursor = cnx.cursor()

    # Consulta SQL para obter os detalhes do exame
    query = """
    SELECT nome_exame, fitc, quantidade1, pe, quantidade2, ecd, quantidade3, 
           pc55, quantidade4, pc7, quantidade5, apc, quantidade6, a700, 
           quantidade7, a750, quantidade8, pb, quantidade9, ko, quantidade10, dupli_pe, 
           dupli1, dupli_a750, dupli2, dupli_pb, dupli3
    FROM exames 
    WHERE id = %s AND ativo = 1
    """
    cursor.execute(query, (id,))
    exame = cursor.fetchone()


    cursor.close()
    cnx.close()

    if exame:
        return render_template('detalhar_exame.html', exame=exame)
    else:
        mensagem_erro = "Exame não encontrado."
        return render_template('exame.html', mensagem_erro=mensagem_erro)










#? Rota para o EXIBE PACIENTE
@app.route('/exibe_paciente')
def exibe_paciente():
    cnx = conectar_banco()
    cursor = cnx.cursor()

    query = """
    SELECT id, nome, prontuario FROM pacientes WHERE ativo = 1
    """
    cursor.execute(query)
    dados_paciente = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('paciente.html', dados_paciente=dados_paciente)

#? Rota para o CRIAR PACIENTE
@app.route('/cria_paciente', methods=['GET', 'POST'])
def cria_paciente():
    if request.method == 'POST':
        # Coletar dados do formulário
        nome = request.form.get('nome')
        prontuario = request.form.get('prontuario')
        id_laboratorio = request.form.get('id_laboratorio')
        quantia_teste = request.form.get('quantia_teste')
        hip_diagnostica = request.form.get('hip_diagnostica')
        obs = request.form.get('obs')
        procedencia = request.form.get('procedencia')
        exames = request.form.get('exames')

        # Inserir dados no banco de dados
        cnx = conectar_banco()
        cursor = cnx.cursor()

        try:
            query = """
            INSERT INTO pacientes (nome, prontuario, id_laboratorio, quantia_teste, 
                                   hip_diagnostica, obs, procedencia, exames, ativo) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (nome, prontuario, id_laboratorio, quantia_teste, hip_diagnostica, obs, procedencia, exames, 1)
            cursor.execute(query, values)
            cnx.commit()
            return redirect(url_for('exibe_paciente'))
        except Exception as e:
            cnx.rollback()
        finally:
            cursor.close()
            cnx.close()

    return render_template('criar_paciente.html')

#? Rota para EDITAR PACIENTE
@app.route('/editar_paciente/<int:id>', methods=['GET', 'POST'])
def editar_paciente(id):
    cnx = conectar_banco()
    cursor = cnx.cursor(dictionary=True)  # Cursor configurado para retornar dicionários

    if request.method == 'POST':
        # Recebe os dados atualizados do formulário
        nome = request.form.get('nome')
        prontuario = request.form.get('prontuario')
        id_laboratorio = request.form.get('id_laboratorio')
        quantia_teste = request.form.get('quantia_teste')
        hip_diagnostica = request.form.get('hip_diagnostica')
        obs = request.form.get('obs')
        procedencia = request.form.get('procedencia')
        exames = request.form.get('exames')

        try:
            # Atualiza os dados do paciente no banco
            query = """
            UPDATE pacientes 
            SET nome = %s, prontuario = %s, id_laboratorio = %s, quantia_teste = %s, 
                hip_diagnostica = %s, obs = %s, procedencia = %s, exames = %s 
            WHERE id = %s
            """
            values = (nome, prontuario, id_laboratorio, quantia_teste, hip_diagnostica, obs, procedencia, exames, id)
            cursor.execute(query, values)
            cnx.commit()
            flash('Paciente atualizado com sucesso!', 'success')
            return redirect(url_for('exibe_paciente'))
        except Exception as e:
            cnx.rollback()
            flash(f'Erro ao atualizar paciente: {e}', 'danger')
        finally:
            cursor.close()
            cnx.close()
    else:
        # Consulta os dados atuais do paciente para preencher o formulário
        query = "SELECT * FROM pacientes WHERE id = %s"
        cursor.execute(query, (id,))
        paciente = cursor.fetchone()
        cursor.close()
        cnx.close()

        if not paciente:
            flash('Paciente não encontrado.', 'danger')
            return redirect(url_for('exibe_paciente'))

        # Renderiza a página com os dados do paciente
        return render_template('mudar_paciente.html', paciente=paciente)

#? Rota para o EXCLUIR PACIENTE
@app.route('/excluir_paciente/<int:id>', methods=['GET'])
def excluir_paciente(id):
    cnx = conectar_banco()
    cursor = cnx.cursor()

    # Marca o paciente como inativo (exclusão lógica)
    query = "UPDATE pacientes SET ativo = 0 WHERE id = %s"
    cursor.execute(query, (id,))
    cnx.commit()

    cursor.close()
    cnx.close()

    return redirect(url_for('exibe_paciente'))

#? Rota para DETALHAR PACIENTE
@app.route('/detalhar_paciente/<int:id>')
def detalhar_paciente(id):
    cnx = conectar_banco()
    cursor = cnx.cursor()

    # Consulta para obter os detalhes do paciente
    query = "SELECT * FROM pacientes WHERE id = %s"
    cursor.execute(query, (id,))
    paciente = cursor.fetchone()

    if not paciente:
        flash('Paciente não encontrado.', 'danger')
        return redirect(url_for('exibe_paciente'))

    # Busca exames associados ao paciente
    cursor.execute("SELECT nome_exame FROM exames WHERE id = %s", (paciente[2],))
    exame = cursor.fetchone()

    cursor.close()
    cnx.close()
    return render_template('detalhar_paciente.html', paciente=paciente, exame=exame)










#? Rota para o EXIBE DESPESA
@app.route('/exibe_despesa')
def exibe_despesa():
    connection = conectar_banco()
    cursor = connection.cursor()
    despesas = []

    try:
        # Consulta para obter as despesas, ordenadas por data
        cursor.execute("SELECT * FROM despesas WHERE ativo = 1 ORDER BY data ASC")
        dados_despesas = cursor.fetchall()

        # Preenche a lista de despesas
        for item in dados_despesas:
            data = item[1]  # Índice da data da despesa
            # Caso a data seja uma string, converte para datetime
            if isinstance(data, str):
                data = datetime.strptime(data, '%Y-%m-%d').date()

            despesas.append({
                'id': item[0],
                'data': data,
                'produtos': item[2],
                'testes': item[3],
                'lote': item[4],
                'validade': item[5],
                'quantia_frascos': item[6],
                'quantia_final': item[7],
                'comprador': item[8],
                'faturamento': item[9],
                'fonte_pagadora': item[10],
                'valor_unitario': item[11],
                'valor_total': item[12],
                'numero_nota': item[13],
                'data_nota': item[14]
            })

    except Exception as e:
        flash(f"Erro ao acessar o banco de dados: {str(e)}", 'error')
        print(f"Erro ao acessar o banco de dados: {e}")
    
    finally:
        cursor.close()
        connection.close()

    return render_template('despesa.html', dados_despesas=despesas)

#? Rota para o CRIAR DESPESA
@app.route('/cria_despesa', methods=['GET', 'POST'])
def cria_despesa():
    if request.method == 'POST':
        # Recebe os dados do formulário
        data = request.form['data']
        produtos = request.form['produtos']
        testes = request.form['testes']
        lote = request.form['lote']
        validade = request.form['validade']
        quantia_frascos = request.form['quantia_frascos']
        quantia_final = request.form['quantia_final']
        comprador = request.form['comprador']
        faturamento = request.form['faturamento']
        fonte_pagadora = request.form['fonte_pagadora']
        valor_unitario = request.form['valor_unitario']
        valor_total = request.form['valor_total']
        numero_nota = request.form['numero_nota']
        data_nota = request.form['data_nota']

        # Insere os dados no banco de dados
        connection = conectar_banco()
        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO despesas (data, produtos, testes, lote, validade, quantia_frascos, quantia_final, 
                                      comprador, faturamento, fonte_pagadora, valor_unitario, valor_total, 
                                      numero_nota, data_nota)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
            (data, produtos, testes, lote, validade, quantia_frascos, quantia_final, comprador, faturamento,
             fonte_pagadora, valor_unitario, valor_total, numero_nota, data_nota)
        )
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('exibe_despesa'))
    else:
        return render_template('criar_despesa.html')

#? Rota para EDITAR DESPESA
@app.route('/editar_despesa/<int:id>', methods=['GET', 'POST'])
def editar_despesa(id):
    if request.method == 'POST':
        # Recebe os dados do formulário
        data = request.form['data']
        produtos = request.form['produtos']
        testes = request.form['testes']
        lote = request.form['lote']
        validade = request.form['validade']
        quantia_frascos = request.form['quantia_frascos']
        quantia_final = request.form['quantia_final']  # Certifique-se de que está definindo esta variável
        comprador = request.form['comprador']
        faturamento = request.form['faturamento']
        fonte_pagadora = request.form['fonte_pagadora']
        valor_unitario = request.form['valor_unitario']
        valor_total = request.form['valor_total']
        numero_nota = request.form['numero_nota']
        data_nota = request.form['data_nota']

        # Atualiza os dados no banco de dados
        connection = conectar_banco()
        cursor = connection.cursor()
        cursor.execute(
            """UPDATE despesas SET data = %s, produtos = %s, testes = %s, lote = %s, validade = %s,
               quantia_frascos = %s, quantia_final = %s, comprador = %s, faturamento = %s,
               fonte_pagadora = %s, valor_unitario = %s, valor_total = %s, numero_nota = %s, 
               data_nota = %s WHERE id = %s""", 
            (data, produtos, testes, lote, validade, quantia_frascos, quantia_final, comprador, faturamento,
             fonte_pagadora, valor_unitario, valor_total, numero_nota, data_nota, id)
        )
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('exibe_despesa'))
    else:
        # Recupera os dados da despesa para edição
        connection = conectar_banco()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM despesas WHERE id = %s", (id,))
        despesa = cursor.fetchone()
        cursor.close()
        connection.close()

        return render_template('mudar_despesa.html', despesa=despesa)

#? Rota para o EXCLUIR DESPESA
@app.route('/excluir_despesa/<int:id>', methods=['GET'])
def excluir_despesa(id):
    # Faz a conexão com o banco de dados.
    connection = conectar_banco()
    cursor = connection.cursor()

    # Atualiza o campo ativo para 0 (exclusão lógica)
    cursor.execute("UPDATE despesas SET ativo = 0 WHERE id = %s", (id,))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for('exibe_despesa'))

#? Rota para DETALHAR DESPESA
@app.route('/detalhar_despesa/<int:id>')
def detalhar_despesa(id):
    connection = conectar_banco()
    cursor = connection.cursor()

    # Recupera os dados da despesa
    cursor.execute("SELECT * FROM despesas WHERE id = %s", (id,))
    despesa = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template('detalhar_despesa.html', despesa=despesa)










#? Rota para o EXIBE USUARIO
@app.route('/exibe_usuarios')
def exibe_usuarios():
    # Verifica se o usuário está logado e se tem permissão (id = 1)
    if 'user_id' not in session or session['user_id'] != 1:
        flash('Você não tem permissão para acessar esta página.', 'error')
        return redirect(url_for('tela_inicial'))

    # Conectar ao banco de dados
    connection = conectar_banco()
    cursor = connection.cursor()
    usuarios = []

    try:
        # Consulta SQL: Ordena primeiro pelos usuários ativos (ativo = 1) e depois pelos inativos (ativo = 0)
        cursor.execute("""
            SELECT id, email, telefone, cpf, cidade, nome_mae, nome_professor, ativo 
            FROM usuarios 
            ORDER BY ativo DESC, nome_mae ASC
        """)
        dados_usuarios = cursor.fetchall()

        # Preenche a lista de usuários com os dados retornados da consulta.
        for item in dados_usuarios:
            usuarios.append({
                'id': item[0],  # ID do usuário
                'email': item[1],  # Email do usuário
                'telefone': item[2],  # Telefone
                'cpf': item[3],  # CPF
                'cidade': item[4],  # Cidade
                'nome_mae': item[5],  # Nome da mãe
                'nome_professor': item[6],  # Nome do professor
                'ativo': item[7]  # Ativo (1 ou 0)
            })

    except Exception as e:
        flash(f"Erro ao acessar o banco de dados: {str(e)}", 'error')

    finally:
        cursor.close()
        connection.close()

    # Retorna a renderização do template 'usuario.html', passando os dados dos usuários.
    return render_template('usuario.html', dados_usuarios=usuarios)



    
#? Rota para o EXCLUIR USUARIO
@app.route('/excluir_usuario/<int:id>', methods=['GET'])
def excluir_usuario(id):
    try:
        # Conectar ao banco de dados
        connection = conectar_banco()
        cursor = connection.cursor()

        # Atualizar o status do usuário para inativo (0) em vez de excluir fisicamente
        cursor.execute("UPDATE usuarios SET ativo = 0 WHERE id = %s", (id,))
        connection.commit()

        flash('Usuário excluído com sucesso.', 'success')

    except Exception as e:
        flash(f"Erro ao excluir o usuário: {str(e)}", 'error')

    finally:
        cursor.close()
        connection.close()

    # Redireciona de volta para a lista de usuários
    return redirect(url_for('exibe_usuarios'))



#? Rota para o DETALHAR USUARIO
@app.route('/detalhar_usuario/<int:id>')
def detalhar_usuario(id):
    connection = conectar_banco()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template('detalhar_usuario.html', usuario=usuario)





# Executa o website
if __name__ == '__main__':
    app.run(debug=True)