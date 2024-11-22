# Guia de Contribuição

Obrigado por considerar contribuir com o projeto **Avalia Django App**! Este documento explica como você pode ajudar a melhorar o projeto, seja corrigindo bugs, adicionando funcionalidades ou melhorando a documentação.

---

## 🛠️ Como Contribuir

### 1. Faça um Fork do Repositório

1. Acesse o repositório original no GitHub.
2. Clique no botão **Fork** no canto superior direito.
3. Clone seu fork localmente:
   ```bash
   git clone https://github.com/suauseu/avalia.git
   cd avalia
   ```

---

### 2. Crie uma Nova Branch

1. Crie uma branch para suas alterações:
   ```bash
   git checkout -b minha-contribuicao
   ```
2. Nomeie a branch de maneira descritiva, como `feature/nova-funcionalidade` ou `fix/erro-login`.

---

### 3. Implemente Suas Alterações

1. **Atualize as Dependências**:  
   Se você adicionar ou atualizar bibliotecas, não se esqueça de atualizar o arquivo `requirements.txt`:
   ```bash
   pip freeze > requirements.txt
   ```

2. **Mantenha a Qualidade do Código**:  
   Utilize as ferramentas configuradas no projeto para formatar e verificar o código:
   ```bash
   isort . && black .
   ```

3. **Testes e Verificação**:  
   - Certifique-se de que suas alterações não quebram o código existente.
   - Adicione ou atualize testes sempre que necessário.

---

### 4. Faça Commits Usando Convenções Padronizadas

Este projeto segue o padrão [Conventional Commits](https://www.conventionalcommits.org/). Utilize os prefixos abaixo para descrever suas alterações:

- **`feat`**: Adição de uma nova funcionalidade.
- **`fix`**: Correção de bugs.
- **`docs`**: Alterações na documentação.
- **`style`**: Alterações de formatação (ex.: espaçamento, indentação).
- **`refactor`**: Alterações no código que não adicionam funcionalidade.
- **`test`**: Adição ou modificação de testes.
- **`chore`**: Atualizações menores ou tarefas de manutenção.

Exemplo:
```bash
git commit -m "feat: adiciona funcionalidade para upload de arquivos PDF"
```

---

### 5. Envie Suas Alterações

1. Envie suas alterações para o GitHub:
   ```bash
   git push origin minha-contribuicao
   ```
2. Abra um **Pull Request** no repositório original.
3. Descreva claramente as alterações realizadas e seu objetivo.

---

## 🎯 Diretrizes Gerais

1. **Documentação**:  
   Certifique-se de que todas as funcionalidades adicionadas ou alteradas estão bem documentadas.

2. **Manter Consistência**:  
   - Utilize a estrutura e o estilo de código já existente no projeto.
   - Evite incluir alterações irrelevantes no Pull Request.

3. **Testes**:  
   - Adicione testes relevantes para qualquer funcionalidade nova.
   - Execute todos os testes para garantir que o código existente não foi quebrado.

4. **Revisão de Código**:  
   Seu Pull Request será revisado por um dos mantenedores antes de ser mesclado. Esteja aberto a sugestões e mudanças.