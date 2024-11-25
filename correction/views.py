from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as loginDjango
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
# LOGIN
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Activity, Answer, Student, Turma
import re
import os
import mimetypes
import time

import docx
# OCR
import easyocr
from PyPDF2 import PdfReader
from ollama import Client



# VIEWS DO LOGIN
def register(request):
    if request.method == "GET":
        context = {"body_class": "register-js"}
        return render(request, "login.html", context)
    else:
        username = request.POST.get("usernameRegister")
        email = request.POST.get("emailRegister")
        password = request.POST.get("passwordRegister")
        confirm_password = request.POST.get("confirmPasswordRegister")
        errors = {}

        if User.objects.filter(email=email).exists():
            messages.error(request, "Este email já está em uso.")
            errors["emailRegister"] = "Este email já está em uso."

        try:
            validate_password(password)  # Valida senha usando regras padrão do Django
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return redirect("login")

        if password != confirm_password:
            errors["passwordRegister"] = "As senhas não coincidem."

        if errors:
            return render(
                request,
                "login.html",
                {
                    "errors": errors,
                    "usernameRegister": username,
                    "emailRegister": email,
                },
            )

        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        user.save()
        messages.success(request, "Usuário criado com sucesso!")

        return render(request, "login.html")


def login(request):
    if request.method == "GET":
        context = {"body_class": "login-js"}
        return render(request, "login.html", context)
    else:
        email = request.POST.get("emailLogin")
        password = request.POST.get("passwordLogin")

        user = authenticate(request, username=email, password=password)

        if user:
            loginDjango(request, user)
            return redirect(home)
        else:
            messages.error(request, "Email ou senha inválidos!")
            return render(request, "login.html")


def logout(request):
    logout(request)
    return redirect("login")


# USUÁRIO
@login_required(login_url="/correction/login")
def user_settings(request):
    return render(request, "user_settings.html", {"user": request.user})


def update_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        newpassword = request.POST.get("newpassword")
        passwordconfirm = request.POST.get("passwordconfirm")

        user = request.user

        # Verifica se já existe um usuário com esse e-mail
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, "Este email já está em uso por outro usuário.")
            return redirect("user_settings")

        # Verifica se a senha atual está correta
        if password and not user.check_password(password):
            messages.error(request, "A senha atual está incorreta!")
            return redirect("user_settings")

        # Verifica se as novas senhas coincidem
        if newpassword and newpassword != passwordconfirm:
            messages.error(request, "As senhas não coincidem!")
            return redirect("user_settings")

        # Atualiza a senha, se fornecida
        if newpassword:
            user.set_password(newpassword)

        user.username = username
        user.email = email
        user.save()

        # Mantém o usuário logado
        if newpassword:
            update_session_auth_hash(request, user)

        messages.success(request, "Usuário atualizado com sucesso!")
        return redirect("user_settings")


@login_required(login_url="/correction/login")
def delete_user(request):
    try:
        request.user.delete()
    except request.user.DoesNotExist:
        # Renderiza uma página com a mensagem de erro
        return render(request, "partials/message.html", status=403)

    return redirect("login")


# VIEWS DA PLATAFORMA
@login_required(login_url="/correction/login")
def home(request):
    turmas = Turma.objects.filter(user=request.user)
    return render(request, "index.html", {"turma": turmas})


@login_required(login_url="/correction/login")
def cursos(request):
    turmas = Turma.objects.filter(user=request.user)
    return render(request, "cursos.html", {"turma": turmas})


@login_required(login_url="/correction/login")
def salvar(request):
    name = request.POST.get("name")
    section = request.POST.get("section")
    Turma.objects.create(name=name, section=section, user=request.user)
    return redirect(home)


@login_required(login_url="/correction/login")
def details(request, id):
    try:
        turma = Turma.objects.get(id=id, user=request.user)
    except Turma.DoesNotExist:
        # Renderiza uma página com a mensagem de erro
        return render(request, "partials/message.html", status=403)

    return render(request, "details.html", {"turma": turma})


@login_required(login_url="/correction/login")
def update(request, id):
    try:
        name = request.POST.get("name")
        section = request.POST.get("section")
        description = request.POST.get("description")
        turma = Turma.objects.get(id=id, user=request.user)
        turma.name = name
        turma.section = section
        turma.description = description
        turma.save()
    except Turma.DoesNotExist:
        # Renderiza uma página com a mensagem de erro
        return render(request, "partials/message.html", status=403)

    return render(request, "details.html", {"turma": turma})


@login_required(login_url="/correction/login")
def delete(request, id):
    try:
        turma = Turma.objects.get(id=id, user=request.user)
        turma.delete()
    except Turma.DoesNotExist:
        # Renderiza uma página com a mensagem de erro
        return render(request, "partials/message.html", status=403)

    return redirect(home)


# ATIVIDADE
@login_required(login_url="/correction/login")
def activities(request, id):
    try:
        id_class = Turma.objects.get(id=id, user=request.user)
        activities = Activity.objects.filter(id_class=id_class)
    except Turma.DoesNotExist:
        # Renderiza uma página com a mensagem de erro
        return render(request, "partials/message.html", status=403)

    return render(
        request, "activities.html", {"activities": activities, "turma": id_class}
    )


@login_required(login_url="/correction/login")
def create_activity(request, id):
    id_class = get_object_or_404(Turma, id=id)
    name = request.POST.get("name")
    description = request.POST.get("description")
    question = request.POST.get("question")

    activity = Activity.objects.create(
        name=name,
        id_class=id_class,
        description=description,
        question=question,
        user=request.user,
    )
    activity.save()
    return redirect("activities", id=id_class.id)


@login_required(login_url="/correction/login")
def select_activity(request, id):
    try:
        activity = Activity.objects.get(id=id, user=request.user)
        students = Student.objects.filter(id_class=activity.id_class)
        answers = Answer.objects.filter(id_activity=id)
    except Activity.DoesNotExist:
        # Renderiza uma página com a mensagem de erro
        return render(request, "partials/message.html", status=403)

    return render(
        request,
        "activityDetails.html",
        {"students": students, "activity": activity, "answers": answers},
    )


@login_required(login_url="/correction/login")
def update_activity(request, id):
    try:
        activity = Activity.objects.get(id=id, user=request.user)

        if request.method == "POST":
            name = request.POST.get("name")
            description = request.POST.get("description")
            question = request.POST.get("question")
            activity.name = name
            activity.description = description
            activity.question = question
            activity.save()
    except Activity.DoesNotExist:
        # Renderiza uma página com a mensagem de erro
        return render(request, "partials/message.html", status=403)

    return redirect("select_activity", id=id)


@login_required(login_url="/correction/login")
def delete_activity(request, id):
    try:
        activity = Activity.objects.get(id=id, user=request.user)
        id_class = activity.id_class.id
        if request.method == "POST":
            activity.delete()
    except Activity.DoesNotExist:
        # Renderiza uma página com a mensagem de erro
        return render(request, "partials/message.html", status=403)

    return redirect("activities", id=id_class)


# Respostas
@login_required(login_url="/correction/login")
def answers(request, id):
    try:
        id_activity = Activity.objects.get(id=id, user=request.user)
        answers = Answer.objects.filter(id_activity=id_activity)
    except Activity.DoesNotExist:
        # Renderiza uma página com a mensagem de erro
        return render(request, "partials/message.html", status=403)

    return render(
        request, "activityDetails.html", {"answers": answers, "activity": id_activity}
    )


@login_required(login_url="/correction/login")
def create_answer(request, id):
    try:
        id_activity = Activity.objects.get(id=id, user=request.user)
    except Activity.DoesNotExist:
        # Renderiza uma página com a mensagem de erro
        return render(request, "partials/message.html", status=403)

    id_student = request.POST.get("id_student")
    student = get_object_or_404(Student, id=id_student)
    studentAnswer = request.FILES.get("studentAnswer")
    extract_value = request.POST.get("extract_value")
    score_raw = request.POST.get("score")
    feedback = request.POST.get("feedback")
    answer_based = request.POST.get("answer_based")
    teacherAnswer = request.POST.get("teacherAnswer")

    # Tratamento do campo score
    score = None
    if score_raw:  # Verifica se o valor foi enviado
        try:
            # Substitui vírgula por ponto, se necessário, e converte para Decimal
            score = Decimal(score_raw.replace(",", "."))
        except (InvalidOperation, AttributeError):
            return HttpResponse(
                "Valor inválido para o campo score. Certifique-se de usar um número válido.",
                status=400,
            )

    answer = Answer.objects.create(
        id_activity=id_activity,
        id_student=student,
        studentAnswer=studentAnswer,
        score=score,
        feedback=feedback,
        extract_value=extract_value,
        user=request.user,
        answer_based=answer_based,
        teacherAnswer=teacherAnswer,
    )
    answer.save()
    return redirect("select_activity", id=id)


@login_required(login_url="/correction/login")
def select_answer(request, id):
    try:
        correction = Answer.objects.get(id=id, user=request.user)
        id_activity = correction.id_activity
        students = Student.objects.filter(id_class=id_activity.id_class)
    except Answer.DoesNotExist:
        # Renderiza uma página com a mensagem de erro
        return render(request, "partials/message.html", status=403)

    return render(
        request, "correction.html", {"answer": correction, "students": students}
    )


@login_required(login_url="/correction/login")
def update_correction(request, id):
    try:
        correction = Answer.objects.get(id=id, user=request.user)
        id_activity = correction.id_activity
        if request.method == "POST":
            id_student = request.POST.get("id_student")
            score = request.POST.get("score")
            feedback = request.POST.get("feedback")
            correction.id_studant = id_student
            correction.score = score
            correction.feedback = feedback
            correction.save()
    except Answer.DoesNotExist:
        # Renderiza uma página com a mensagem de erro
        return render(request, "partials/message.html", status=403)

    return redirect("select_activity", id=id_activity.id)


@login_required(login_url="/correction/login")
def delete_correction(request, id):
    try:
        correction = Answer.objects.get(id=id, user=request.user)
        id_activity = correction.id_activity.id
        if request.method == "POST":
            correction.delete()
    except Answer.DoesNotExist:
        # Renderiza uma página com a mensagem de erro
        return render(request, "partials/message.html", status=403)

    return redirect("select_activity", id=id_activity)


# Students
@login_required(login_url="/correction/login")
def students(request, id):
    try:
        id_class = Turma.objects.get(id=id, user=request.user)
        students = Student.objects.filter(id_class=id_class)
    except Turma.DoesNotExist:
        # Renderiza uma página com a mensagem de erro
        return render(request, "partials/message.html", status=403)

    return render(request, "students.html", {"students": students, "turma": id_class})


@login_required(login_url="/correction/login")
def create_student(request, id):
    try:
        id_class = Turma.objects.get(id=id, user=request.user)
        name = request.POST.get("name")
        email = request.POST.get("email")

        student = Student.objects.create(
            name=name, id_class=id_class, email=email, user=request.user
        )
        student.save()
    except Turma.DoesNotExist:
        # Renderiza uma página com a mensagem de erro
        return render(request, "partials/message.html", status=403)

    return redirect("students", id=id_class.id)


@login_required(login_url="/correction/login")
def select_student(request, id):
    try:
        student = Student.objects.get(id=id, user=request.user)
    except Student.DoesNotExist:
        # Renderiza uma página com a mensagem de erro
        return render(request, "partials/message.html", status=403)

    return render(request, "studentDetails.html", {"student": student})


@login_required(login_url="/correction/login")
def update_student(request, id):
    try:
        student = Student.objects.get(id=id, user=request.user)
        if request.method == "POST":
            name = request.POST.get("name")
            email = request.POST.get("email")
            id_class = student.id_class.id
            student.name = name
            student.email = email
            student.save()
            return redirect("students", id=id_class)
        else:
            return render(request, "studentDetails.html", {"student": student})
    except Student.DoesNotExist:
        # Renderiza uma página com a mensagem de erro
        return render(request, "partials/message.html", status=403)


@login_required(login_url="/correction/login")
def delete_student(request, id):
    try:
        student = Student.objects.get(id=id, user=request.user)
        if request.method == "POST":
            id_class = student.id_class.id
            student.delete()
    except Student.DoesNotExist:
        # Renderiza uma página com a mensagem de erro
        return render(request, "partials/message.html", status=403)

    return redirect("students", id=id_class)





def extract_text_from_pdf(pdf_path):
    """
    Extrai texto puro de um arquivo PDF usando PyPDF2
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += (
                page.extract_text() or ""
            )  # Combina textos extraídos de todas as páginas
        return text.strip()
    except Exception as e:
        print(f"Erro ao extrair texto do PDF: {e}")
        return ""


# Configuração de tamanho máximo de arquivo permitido (em bytes, aqui 50MB)
MAX_FILE_SIZE = 50 * 1024 * 1024


# Funções de extração de texto por tipo de arquivo
def extract_text_from_image(file_path):
    """Extrai texto de uma imagem usando EasyOCR."""
    reader = easyocr.Reader(["pt", "en"])
    result = reader.readtext(file_path, detail=0)
    return " ".join(result)


def extract_text_from_pdf(file_path):
    """Extrai texto de um arquivo PDF usando PyPDF2."""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        # Remove quebras de linha desnecessárias
        return " ".join(text.split())
    except Exception as e:
        raise ValueError(f"Erro ao processar o PDF: {e}")


def extract_text_from_txt(file_path):
    """Extrai texto de um arquivo TXT."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except Exception as e:
        raise ValueError(f"Erro ao processar o arquivo TXT: {e}")


def extract_text_from_word(file_path):
    """Extrai texto de um arquivo Word (docx)."""
    try:
        doc = docx.Document(file_path)
        return " ".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        raise ValueError(f"Erro ao processar o arquivo Word: {e}")


def validate_file(uploaded_file):
    """
    Valida tipo e tamanho do arquivo.
    """
    # Verifica o tamanho do arquivo
    if uploaded_file.size > MAX_FILE_SIZE:
        raise ValueError("O arquivo excede o tamanho máximo permitido de 50MB.")

    # Verifica o tipo MIME
    mime_type, _ = mimetypes.guess_type(uploaded_file.name)
    valid_mime_types = [
        "image/",  # Imagens
        "application/pdf",  # PDF
        "text/plain",  # TXT
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # Word (docx)
    ]
    if not mime_type or not any(
        mime_type.startswith(valid) for valid in valid_mime_types
    ):
        raise ValueError(
            f"Tipo de arquivo não suportado: {mime_type or 'desconhecido'}."
        )


def extract_text_from_file(file_path, mime_type):
    """
    Identifica o tipo do arquivo e delega a extração de texto para a função apropriada.
    """
    if mime_type.startswith("image/"):
        return extract_text_from_image(file_path)
    elif mime_type == "application/pdf":
        return extract_text_from_pdf(file_path)
    elif mime_type == "text/plain":
        return extract_text_from_txt(file_path)
    elif (
        mime_type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        return extract_text_from_word(file_path)
    else:
        raise ValueError(f"Tipo de arquivo não suportado: {mime_type}")


def extract_text(request):
    """
    Extrai texto de arquivos enviados pelo usuário.
    Suporta imagens, PDFs, arquivos TXT e Word.
    """
    if request.method != "POST" or not request.FILES.get("studentAnswer"):
        return HttpResponse("Nenhum arquivo fornecido.", status=400)

    uploaded_file = request.FILES["studentAnswer"]

    try:
        # Validação do arquivo
        validate_file(uploaded_file)

        # Salva o arquivo temporariamente
        file_path = f"media/uploads/{uploaded_file.name}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb+") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Extrai o texto do arquivo
        mime_type, _ = mimetypes.guess_type(file_path)
        extracted_text = extract_text_from_file(file_path, mime_type)

        # Remove o arquivo temporário após o uso
        os.remove(file_path)

        # Obtém informações adicionais da requisição
        question = request.POST.get("question", "Qual a cor da casa amarela da minha rua?")
        teacherAnswer = request.POST.get("teacherAnswer", "")

        # Chama a função de correção
        score, feedback, error_message = correction(question, extracted_text, teacherAnswer)
        # Verifica se houve um erro na função de correção
        if error_message:
            raise Exception(error_message)
        
        return JsonResponse(
            {"score": score, "feedback": feedback, "extract_value": extracted_text},
            status=200,
        )

    except ValueError as e:
        return HttpResponse(str(e), status=400)

    except Exception as e:
        return HttpResponse(f"Erro interno do servidor: {e}", status=500)


def correction(question, answer, teacherAnswer):
    """
    Função para corrigir respostas de alunos usando o Ollama com critérios atualizados.

    Args:
        question (str): Enunciado da questão.
        answer (str): Resposta do aluno.
        teacherAnswer (str): Resposta padrão fornecida pelo professor.

    Returns:
        tuple: (score, feedback, error_message)
            - score: Nota atribuída (float) ou None em caso de erro.
            - feedback: Feedback gerado (str) ou None em caso de erro.
            - error_message: Mensagem de erro (str) ou None se não houve erro.
    """
    print("Iniciando correção...")

    # Prompt atualizado com os novos critérios e exemplos
    content = f"""
    **Contexto:**

    Você é um corretor altamente especializado em avaliação de atividades educacionais em português do Brasil. Sua tarefa é corrigir respostas de alunos com base no enunciado fornecido e, quando disponível, na resposta base do professor. Suas respostas devem ser precisas, objetivas e baseadas estritamente nas informações fornecidas. Não inclua informações adicionais, opiniões ou justificativas irrelevantes.

    **Tarefas:**

    1. **Validação da Entrada:**

       - Verifique se o enunciado e a resposta do aluno são claros e válidos.
       - Se o enunciado ou a resposta do aluno não forem válidos ou estiverem incompreensíveis, atribua nota **0.0**.
       - No feedback, responda exatamente: "O enunciado ou a resposta fornecida não são válidos."

    2. **Avaliação da Resposta do Aluno:**

       - Compare a resposta do aluno com o enunciado e, se disponível, com a resposta base do professor.
       - Avalie a coerência, correção e completude da resposta em relação ao enunciado.
       - Para questões que exigem precisão absoluta (ex.: cálculos ou respostas exatas), atribua nota **0.0** se a resposta estiver incorreta.
       - Para perguntas abertas (ex.: nomes, conceitos), atribua nota máxima para respostas corretas, mesmo que contenham detalhes adicionais.
       - Atribua uma nota parcial se a resposta demonstrar entendimento parcial, mas contiver pequenos erros.

    3. **Atribuição de Nota:**

       - **Correção:** A resposta está tecnicamente correta e alinhada ao solicitado no enunciado? Respostas corretas devem receber nota máxima, independentemente de estilo ou sugestões adicionais.
       - **Completude:** A resposta cobre todos os aspectos explicitamente exigidos no enunciado? Não penalize por informações ausentes que não foram solicitadas.
       - **Clareza:** A resposta é compreensível? Sugestões de estilo, como concisão, devem ser incluídas apenas no feedback e não devem impactar a nota.

    4. **Geração de Feedback:**

       - Explique o motivo da nota de forma clara e concisa.
       - Críticas ou sugestões que extrapolem o escopo do enunciado devem ser apenas mencionadas no feedback e não devem penalizar a nota.

    **Formato Estrito da Resposta:**

    - Nota: [Número entre 0.0 e 10.0, com no máximo uma casa decimal; ex.: 0.0, 9.5, 10.0]
    - Feedback: [Descrição objetiva, clara, direta e concisa. Não inclua informações irrelevantes.]

    **IMPORTANTE:** Sua resposta **deve** seguir exatamente o formato especificado: primeiro "Nota:" seguido da nota, depois "Feedback:" seguido do feedback. Não inclua informações adicionais.

    **Exemplos:**

    1. **Entrada Inválida:**

       - **Enunciado:** (texto ilegível ou ausente)
       - **Resposta do aluno:** 42.
       - **Resposta base do professor:** Não fornecida.
       - **Saída Esperada:**
         - Nota: 0.0
         - Feedback: O enunciado ou a resposta fornecida não são válidos.

    2. **Pergunta Objetiva Correta:**

       - **Enunciado:** Quanto é 2+2?
       - **Resposta do aluno:** 4.
       - **Resposta base do professor:** 4.
       - **Saída Esperada:**
         - Nota: 10.0
         - Feedback: A resposta está correta. O aluno indicou corretamente que 2+2 é 4.

    3. **Pergunta Objetiva Incorreta:**

       - **Enunciado:** Quanto é 2+2?
       - **Resposta do aluno:** 5.
       - **Resposta base do professor:** 4.
       - **Saída Esperada:**
         - Nota: 0.0
         - Feedback: A resposta está incorreta. O resultado correto de 2+2 é 4.

    4. **Pergunta Aberta com Erro de Grafia:**

       - **Enunciado:** Quem descobriu o Brasil?
       - **Resposta do aluno:** Pedro Álvares Cabaral.
       - **Resposta base do professor:** Pedro Álvares Cabral.
       - **Saída Esperada:**
         - Nota: 8.0
         - Feedback: A resposta demonstra entendimento, mas contém um erro de grafia no nome "Cabral".

    5. **Resposta com Detalhes Adicionais:**

       - **Enunciado:** Qual é a cor da casa amarela?
       - **Resposta do aluno:** A casa é amarela como o sol brilhante.
       - **Resposta base do professor:** Amarela.
       - **Saída Esperada:**
         - Nota: 10.0
         - Feedback: A resposta está correta. Embora contenha detalhes extras, está alinhada com o enunciado.

    **Entrada:**

    - **Enunciado da atividade:** {question}
    - **Resposta do aluno:** {answer}
    - **Resposta base do professor:** {teacherAnswer if teacherAnswer else "Não fornecida"}
    """

    # Chamar a função de comunicação com o modelo
    result, error_message, processing_time = ollama_chat(model="mistral", content=content)

    # Imprimir a resposta bruta do modelo para depuração
    print("Resposta bruta do modelo:", repr(result))

    # Logs detalhados agrupados em um único bloco
    logs = f"""
    ======== CORREÇÃO INICIADA ========
    [ENUNCIADO]
    {question}

    [RESPOSTA DO ALUNO]
    {answer}

    [RESPOSTA BASE DO PROFESSOR]
    {teacherAnswer if teacherAnswer else "Não fornecida"}

    ======== RESPOSTA DO MODELO ========
    {result}

    ======== TEMPO DE PROCESSAMENTO ========
    {processing_time:.2f} segundos

    ======== MENSAGEM DE ERRO ========
    {error_message if error_message else "Nenhum erro encontrado"}

    ======== CORREÇÃO FINALIZADA ========
    """
    print(logs)

    # Expressões regulares melhoradas
    match = re.search(r"\s*Nota\s*:\s*([0-9]+(?:\.[0-9]+)?)", result, re.IGNORECASE)
    feedback_match = re.search(r"\s*Feedback\s*:\s*(.+)", result, re.DOTALL | re.IGNORECASE)

    if match and feedback_match:
        try:
            # Converter a nota para float com até uma casa decimal
            score = round(float(match.group(1)), 1)
            feedback = feedback_match.group(1).strip()

            return score, feedback, None

        except ValueError:
            return None, result.strip(), "Erro ao converter a nota."

    # Caso a resposta seja exatamente o feedback padrão para entradas inválidas
    if "O enunciado ou a resposta fornecida não são válidos." in result:
        return 0.0, "O enunciado ou a resposta fornecida não são válidos.", None

    # Resposta inesperada sem nota ou feedback
    return None, result.strip(), "Resposta inesperada. Não foi possível processar."

def ollama_chat(model, content):
    """
    Função para interagir com o modelo Ollama.

    Args:
        model (str): Nome do modelo.
        content (str): Conteúdo da solicitação.

    Returns:
        tuple: (result, error_message, processing_time)
            - result: Resposta do modelo.
            - error_message: Mensagem de erro, se houver.
            - processing_time: Tempo em segundos para processar a solicitação.
    """
    from ollama import Client

    client = Client()
    start_time = time.time()

    try:
        response = client.chat(model=model, messages=[{"role": "user", "content": content}])
        end_time = time.time()

        result = response.get('message', {}).get('content', '')
        processing_time = end_time - start_time
        return result, None, processing_time

    except Exception as e:
        end_time = time.time()
        processing_time = end_time - start_time
        return None, str(e), processing_time
