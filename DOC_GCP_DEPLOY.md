# Deploy de Aplicação Django no Google Cloud (VM com Docker)

Este documento descreve como realizar o deploy de uma nova versão da aplicação **Avalia** em uma VM no **Google Cloud**, utilizando o branch `main` como referência.

---

## **Fluxo de Deploy**

1. **Acesse a VM no Google Cloud**
   - Use o **gcloud** ou a interface do console do Google Cloud para conectar-se à VM.

2. **Navegue até a pasta do projeto**
   - O projeto está localizado em:
     ```
     /home/{USER}/avalia-project/avalia
     ```

3. **Atualize o código do branch `main`**
   - No diretório do projeto, atualize o código com o branch `main`.

4. **Reinicie o container com a nova versão**
   - Execute o comando:
     ```bash
     make deploy
     ```

---

## **Comandos Úteis**

- **Ver logs da aplicação**
  ```bash
  make docker-logs
  ```
---

## **Notas**
- O branch `main` é utilizado como referência para o deploy.
- O ciclo de deploy recompila a imagem e reinicia o container automaticamente.