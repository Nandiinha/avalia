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
import requests

import mimetypes



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
            raise ValueError(error_message)
        
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
    Função para corrigir respostas de alunos usando o Ollama.

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
    print("Chegou na função correction")

    if len(teacherAnswer) > 0:
        content = f"""
            Você será um corretor de atividades. Sua tarefa é avaliar a resposta do aluno com base no enunciado da atividade, verificando se a resposta está correta, coerente e dentro do contexto do enunciado. 

            Siga estas diretrizes:  
            1. Leia o enunciado da atividade e a resposta fornecida pelo aluno.  
            2. Verifique se a resposta do aluno faz sentido com o enunciado e se está correta.  
            3. Caso a resposta esteja fora do contexto ou não faça sentido com o enunciado, desconsidere a resposta e atribua nota zero.  
            4. Atribua uma nota de 0 a 10 baseada na correção, clareza e completude da resposta.  
            5. Forneça um feedback explicando o motivo da nota, destacando acertos e apontando os erros ou lacunas na resposta.  

            Formato de entrada:  
            - Enunciado da atividade: {question}
            - Resposta do aluno: {answer} 

            Formato de saída:  
            - Nota: [0-10]  
            - Feedback: [Comentário explicativo sobre a nota]

            Certifique-se de manter a avaliação justa e bem fundamentada.  
        """
    else:
        content = f"""
            Você será um corretor de atividades com base em uma resposta padrão fornecida pelo professor. Sua tarefa é comparar a resposta do aluno com a resposta base e avaliar sua precisão, clareza e alinhamento.

            Siga estas diretrizes:

            Leia a resposta base fornecida pelo professor e a resposta do aluno.
            Verifique se a resposta do aluno está alinhada com a resposta base.
            Se houver inconsistências, erros ou falta de alinhamento com a resposta base, destaque-os.
            Caso a resposta do aluno esteja fora do contexto da resposta base, desconsidere-a e atribua nota zero.
            A resposta base fornecida pelo professor deve ser considerada como verdade e referência principal para a correção.
            Atribua uma nota de 0 a 10 baseada na adequação da resposta do aluno à resposta base.
            Forneça um feedback explicando o motivo da nota, destacando acertos e apontando os erros ou lacunas na resposta.
            Formato de entrada:

            Resposta base do professor: {teacherAnswer}
            Resposta do aluno: {answer}
            
            Formato de saída:
            Nota: [0-10]
            Feedback: [Comentário explicativo sobre a nota]
            Certifique-se de seguir rigorosamente a resposta base como referência, sem incluir interpretações externas.
        """

    # Chamar a função de comunicação com o Ollama
    result, error_message = ollama_chat(model="mistral", content=content)

    if error_message:
        return None, None, error_message

    # Extrair a nota da resposta usando regex
    match = re.search(r"\d+(\.\d+)?", result)
    if match:
        try:
            score = float(match.group())
        except ValueError:
            print("Erro ao converter a resposta para um número. Resposta recebida:", result)
            return None, result, "Erro ao converter a resposta para um número."
    else:
        print("Nenhum número encontrado na resposta. Resposta recebida:", result)
        return None, result, "Nenhum número encontrado na resposta."

    print("Nota:", score)
    print("Retorno:", result)
    return score, result, None

def ollama_chat(model, content):
    """
    Função síncrona para enviar mensagens ao Ollama com streaming habilitado.

    Args:
        model (str): Nome do modelo (e.g., "mistral").
        content (str): Conteúdo da mensagem para o Ollama.

    Returns:
        tuple: (result, error_message)
            - result: Resposta completa do Ollama (str) ou None em caso de erro.
            - error_message: Mensagem de erro (str) ou None se não houve erro.
    """
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    
    try:
        # Inicializa o cliente do Ollama com o host configurado
        client = Client(host=OLLAMA_HOST)

        # Chamar a API do Ollama com streaming
        stream = client.chat(
            model=model,
            messages=[{"role": "user", "content": content}],
            stream=True
        )

        # Iterar sobre o stream e construir a resposta
        result = ""
        for chunk in stream:
            result += chunk["message"]["content"]  # Acessa o conteúdo do chunk

        return result, None

    except Exception as e:
        error_message = f"Erro ao comunicar-se com o Ollama no endereço {OLLAMA_HOST}: {str(e)}"
        print(error_message)
        return None, error_message