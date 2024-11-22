# Fluxo de Trabalho com Git

Siga estes passos para contribuir com o projeto **Avalia Django App**:

1. **Faça um Fork e Clone o Repositório.**
2. **Crie uma Branch descritiva** para suas alterações.
3. **Implemente e Commite suas Alterações** seguindo o padrão [Conventional Commits](https://www.conventionalcommits.org/).
4. **Sincronize sua Branch** com as mudanças mais recentes do repositório principal.
5. **Envie as Alterações** para o seu fork.
6. **Abra um Pull Request** e descreva as alterações realizadas.

---

## ⚠️ Ignorar Hooks de Pré-Commit (Quando Necessário)

Os hooks de pré-commit, como verificações de formatação (`black`, `isort`) ou outras validações, podem impedir um commit caso o código não esteja formatado ou siga padrões específicos. Nesses casos, você pode corrigir o problema ou, se necessário, forçar o commit ignorando os hooks:

```bash
git commit --no-verify -m "sua mensagem"
```

**Quando Usar?**
- **Problemas com ferramentas de formatação:** Como `black` ou `isort`, que detectaram problemas no código.
- **Commit urgente:** Quando o tempo é crítico e as validações podem ser ajustadas depois.

**Nota:** Esta é uma saída forçada e deve ser usada com cautela. Sempre revise o código antes de abrir um Pull Request para garantir que ele segue os padrões do projeto.