import mimetypes
import os
import re
from decimal import Decimal, InvalidOperation

import docx
import easyocr
from django.contrib.auth import authenticate
from django.contrib.auth import login as loginDjango
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from PyPDF2 import PdfReader

from .models import Activity, Answer, Student, Turma


# VIEWS DO LOGIN
def register(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request.POST.get("usernameRegister")
        email = request.POST.get("emailRegister")
        password = request.POST.get("passwordRegister")

        if User.objects.filter(email=email).exists():
            return HttpResponse("Já existe um usuário com esse email")

        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        user.save()

        return HttpResponse("Usuário criado com sucesso!")


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        email = request.POST.get("emailLogin")
        password = request.POST.get("passwordLogin")

        user = authenticate(request, username=email, password=password)

        if user:
            loginDjango(request, user)
            return redirect(home)
        else:
            return HttpResponse("email ou senha inválidos")


@login_required(login_url="/correction/login")
def plataform(request):
    return HttpResponse("Plataforma")


# VIEWS DA PLATAFORMA
def home(request):
    turma = Turma.objects.all()
    return render(request, "index.html", {"turma": turma})


def cursos(request):
    turma = Turma.objects.all()
    return render(request, "cursos.html", {"turma": turma})


def salvar(request):
    name = request.POST.get("name")
    section = request.POST.get("section")
    Turma.objects.create(name=name, section=section)
    turma = Turma.objects.all()
    return redirect(home)


def details(request, id):
    turma = Turma.objects.get(id=id)
    return render(request, "details.html", {"turma": turma})


def update(request, id):
    name = request.POST.get("name")
    section = request.POST.get("section")
    description = request.POST.get("description")
    turma = Turma.objects.get(id=id)
    turma.name = name
    turma.section = section
    turma.description = description
    turma.save()
    return render(request, "details.html", {"turma": turma})


def delete(request, id):
    turma = Turma.objects.get(id=id)
    turma.delete()
    return redirect(home)


# ATIVIDADE
def activities(request, id):
    id_class = get_object_or_404(Turma, id=id)
    activities = Activity.objects.filter(id_class=id_class)
    return render(
        request, "activities.html", {"activities": activities, "turma": id_class}
    )


def create_activity(request, id):
    id_class = get_object_or_404(Turma, id=id)
    name = request.POST.get("name")
    description = request.POST.get("description")
    question = request.POST.get("question")

    activity = Activity.objects.create(
        name=name, id_class=id_class, description=description, question=question
    )
    activity.save()
    return redirect("activities", id=id_class.id)


def select_activity(request, id):
    activity = get_object_or_404(Activity, id=id)
    students = Student.objects.filter(id_class=activity.id_class)
    answers = Answer.objects.filter(id_activity=id)
    return render(
        request,
        "activityDetails.html",
        {"students": students, "activity": activity, "answers": answers},
    )


def update_activity(request, id):
    activity = Activity.objects.get(id=id)

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        question = request.POST.get("question")
        activity.name = name
        activity.description = description
        activity.question = question
        activity.save()
    return redirect("select_activity", id=id)


def delete_activity(request, id):
    activity = Activity.objects.get(id=id)
    id_class = activity.id_class.id
    if request.method == "POST":
        activity.delete()
    return redirect("activities", id=id_class)


# Respostas
def answers(request, id):
    id_activity = get_object_or_404(Activity, id=id)
    answers = Answer.objects.filter(id_activity=id_activity)
    return render(
        request, "activityDetails.html", {"answers": answers, "activity": id_activity}
    )


def create_answer(request, id):
    id_activity = get_object_or_404(Activity, id=id)
    id_student = int(request.POST.get("id_student"))
    student = get_object_or_404(
        Student, id=id_student
    )  # Substitua pela busca do modelo Student

    studentAnswer = request.FILES.get("studentAnswer")
    extract_value = request.POST.get("extract_value")
    score_raw = request.POST.get("score")
    feedback = request.POST.get("feedback")

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
    )
    answer.save()
    return redirect("select_activity", id=id)


def select_answer(request, id):
    correction = get_object_or_404(Answer, id=id)
    id_activity = correction.id_activity
    students = Student.objects.filter(id_class=id_activity.id_class)
    return render(
        request, "correction.html", {"answer": correction, "students": students}
    )


def update_correction(request, id):
    correction = get_object_or_404(Answer, id=id)
    id_activity = correction.id_activity
    # students = Student.objects.filter(id_class=id_activity.id_class)

    if request.method == "POST":
        id_student = request.POST.get("id_student")
        score = request.POST.get("score")
        feedback = request.POST.get("feedback")
        correction.id_studant = id_student
        correction.score = score
        correction.feedback = feedback
        correction.save()

    return redirect("select_activity", id=id_activity.id)


def delete_correction(request, id):
    correction = get_object_or_404(Answer, id=id)
    id_activity = correction.id_activity.id
    if request.method == "POST":
        correction.delete()
    return redirect("select_activity", id=id_activity)


# Students
def students(request, id):
    id_class = Turma.objects.get(id=id)
    students = Student.objects.filter(id_class=id_class)
    return render(request, "students.html", {"students": students, "turma": id_class})


def create_student(request, id):
    id_class = get_object_or_404(Turma, id=id)
    name = request.POST.get("name")
    email = request.POST.get("email")

    student = Student.objects.create(name=name, id_class=id_class, email=email)
    student.save()
    return redirect("students", id=id_class.id)


def select_student(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, "studentDetails.html", {"student": student})


def update_student(request, id):
    student = get_object_or_404(Student, id=id)
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


def studentDetails(request, id):
    student = Student.objects.get(id=id)
    return render(request, "studentDetails.html", {"student": student})


def delete_student(request, id):
    if request.method == "POST":
        student = get_object_or_404(Student, id=id)
        id_class = student.id_class.id
        student.delete()
        # Redireciona para a URL de lista de estudantes, passando o ID da turma
        return redirect("students", id=id_class)
    # Caso não seja um POST, pode retornar um erro ou redirecionar para uma página de erro
    return redirect("students", id=id_class)


import mimetypes
import os
import re

import docx
# OCR
import easyocr
import ollama  # Certifique-se de que a biblioteca está importada corretamente
from django.http import HttpResponse, JsonResponse
from PyPDF2 import PdfReader


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
        question = request.POST.get("question", "").strip()
        # student_name = request.POST.get('studentName', '').strip()

        # Chama a função de correção
        score, feedback = correction(question, extracted_text)

        return JsonResponse(
            {"score": score, "feedback": feedback, "extract_value": extracted_text},
            status=200,
        )

    except ValueError as e:
        return HttpResponse(str(e), status=400)

    except Exception as e:
        return HttpResponse(f"Erro interno do servidor: {e}", status=500)


def correction(question, answer):
    content = f"Com base na pergunta: {question}. Verifique se a resposta a seguir está correta: {answer}. É importante que a resposta se adeque ao que está sendo perguntado, se fungir do tema da pergunta retorne uma nota baixa mesmo que a resposta esteja correta em um outro contexto. Responda dando um feedback e uma nota de 0 a 10. Desconsidere erros gramaticais para a realização da correção."

    stream = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": content}],
        stream=True,
    )

    response = ""
    for chunk in stream:
        response += chunk["message"]["content"]

    # Use regex para extrair o número da resposta, se houver
    match = re.search(r"\d+(\.\d+)?", response)  # Procura um número inteiro ou decimal
    if match:
        try:
            score = float(match.group())  # Converte o número extraído para float
        except ValueError:
            print(
                "Erro ao converter a resposta para um número. Resposta recebida:",
                response,
            )
            score = None
    else:
        print("Nenhum número encontrado na resposta. Resposta recebida:", response)
        score = None

    print("Nota:", score)
    print("Retorno:", response)
    return score, response  # Retorna a nota
