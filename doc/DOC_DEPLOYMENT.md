# Deployment no Vercel

Este documento explica como configurar e realizar o deploy do projeto **Avalia Django App** na plataforma **Vercel**.

---

## Pré-requisitos

Antes de começar, certifique-se de ter:

1. Uma conta no Vercel ([criar aqui](https://vercel.com/)).
2. O CLI do Vercel instalado:
   ```bash
   npm install -g vercel
   ```
3. O projeto configurado localmente e funcional.

---

## Configuração do Projeto

### Arquivos Necessários

1. **`vercel.json`**  
   Coloque o seguinte arquivo na raiz do projeto:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "build_files.sh",
         "use": "@vercel/static-build",
         "config": { "distDir": "staticfiles" }
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "build_files.sh"
       }
     ]
   }
   ```

2. **`build_files.sh`**  
   Este script prepara o ambiente para o deploy:
   ```bash
   #!/bin/bash
   echo "Building the project..."
   python3.9 -m pip install -r requirements.txt
   python3.9 manage.py collectstatic --no-input
   python3.9 manage.py migrate
   ```
   Torne o script executável:
   ```bash
   chmod +x build_files.sh
   ```

---

## Configuração de Variáveis de Ambiente

No painel do Vercel, adicione as seguintes variáveis:

- `DJANGO_ENV`: `production`
- `DJANGO_SECRET_KEY`: Gere uma chave segura com:
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe())"
  ```
- `ALLOWED_HOSTS`: Inclua os domínios permitidos, como `seusite.com,vercel.app`.
- `DEBUG`: `False`

---

## Fazendo o Deploy

### Usando o Painel do Vercel

1. Acesse o [Painel do Vercel](https://vercel.com/dashboard).
2. Clique em **New Project** e conecte o repositório.
3. Adicione as variáveis de ambiente mencionadas.
4. Clique em **Deploy**.

### Usando o CLI do Vercel

1. Autentique-se no Vercel:
   ```bash
   vercel login
   ```
2. Execute o comando de deploy:
   ```bash
   vercel
   ```
3. Siga as instruções interativas.

---

## Pós-Deploy

### Verificar o Deploy

1. Após o deploy, acesse o URL gerado (ex.: `https://seusite.vercel.app`).
2. Verifique se a aplicação está funcionando corretamente.

### Resolver Problemas Comuns

- **Arquivos estáticos não carregam**: Verifique se `collectstatic` foi executado corretamente no `build_files.sh`.
- **Erro 500**: Confirme as variáveis de ambiente e revise os logs no painel do Vercel.
- **Erros de configuração**: Confira as chaves `DJANGO_SECRET_KEY` e `ALLOWED_HOSTS`.

---

## Atualizando o Deploy

Para atualizar o deploy após alterações no projeto:

1. Faça commit e push das mudanças no repositório.
2. O Vercel detectará automaticamente e iniciará um novo deploy.
3. Verifique o URL para confirmar a atualização.

---

## Referências

- [Documentação do Vercel](https://vercel.com/docs)
- [Documentação do Django](https://docs.djangoproject.com/)
