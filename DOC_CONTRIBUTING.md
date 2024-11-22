# Guia de Contribuição

Obrigado por considerar contribuir com o projeto **Avalia Django App**! Siga as orientações abaixo para colaborar de maneira eficiente.

---

## 🛠️ Como Contribuir

1. **Faça um Fork e Clone do Repositório**  
   - Realize um fork no GitHub e clone localmente:
     ```bash
     git clone https://github.com/seuusuario/avalia.git
     cd avalia
     ```

2. **Crie uma Branch**  
   - Use uma branch descritiva para suas alterações, como `feature/nova-funcionalidade` ou `fix/erro-login`.

3. **Implemente Suas Alterações**  
   - Formate e verifique o código:
     ```bash
     isort . && black .
     ```
   - Atualize dependências, se necessário:
     ```bash
     pip freeze > requirements.txt
     ```
   - Certifique-se de que suas alterações não quebram o código existente.

4. **Siga o Fluxo de Trabalho com Git**  
   Para detalhes sobre como gerenciar o fluxo de trabalho com Git, veja o arquivo [DOC_GIT_WORKFLOW.md](./DOC_GIT_WORKFLOW.md).

5. **Envie e Abra um Pull Request**  
   - Faça o push das alterações para o seu fork:
     ```bash
     git push origin minha-branch
     ```
   - Abra um Pull Request no repositório original, explicando as alterações realizadas.

---

## 🎯 Diretrizes Gerais

1. **Documentação**: Atualize a documentação para qualquer funcionalidade ou alteração relevante.
2. **Manter Consistência**: Siga o estilo e a estrutura de código do projeto.
3. **Testes**: Adicione ou atualize testes para garantir que sua alteração não introduza bugs.
4. **Revisão**: O Pull Request será revisado antes de ser aceito. Esteja aberto a sugestões.
