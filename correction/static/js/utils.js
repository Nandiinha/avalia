/**
 * Exibe uma mensagem de erro ou sucesso usando Toast ou Alert do Bootstrap.
 * @param {Object} options - Objeto contendo os parâmetros da mensagem.
 * @param {string} options.message - Mensagem a ser exibida.
 * @param {string} options.type - Tipo de exibição: "toast" ou "alert".
 * @param {string} options.severity - Severidade: "error" ou "success".
 * @param {string} [options.containerId] - ID do container onde o Alert será exibido (necessário para Alert).
 */
function showMessage({ message, type, severity, containerId }) {
    const severityClass = severity === 'success' ? 'alert-success' : 'alert-danger';

    if (type === 'toast') {
        // Verifica se o container já existe, se não, cria-o
        let toastContainer = document.getElementById('toastContainer');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toastContainer';
            toastContainer.style.position = 'fixed';
            toastContainer.style.top = '20px';
            toastContainer.style.right = '20px';
            toastContainer.style.zIndex = '1050';
            document.body.appendChild(toastContainer);
        }

        // Cria o conteúdo do toast
        const toastHtml = `
            <div class="toast" data-delay="5000">
                <div class="toast-header ${severity === 'success' ? 'bg-success' : 'bg-danger'} text-white">
                    <strong class="mr-auto">${severity === 'success' ? 'Sucesso' : 'Erro'}</strong>
                    <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Fechar">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="toast-body">${message}</div>
            </div>
        `;

        const toastElement = document.createElement('div');
        toastElement.innerHTML = toastHtml;
        toastContainer.appendChild(toastElement.firstElementChild);

        const toast = new bootstrap.Toast(toastElement.firstElementChild);
        toast.show();

        // Remover automaticamente após exibição
        toastElement.firstElementChild.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    } else if (type === 'alert') {
        const alertHtml = `
            <div class="alert ${severityClass} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="close" data-dismiss="alert" aria-label="Fechar">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
        `;

        if (containerId) {
            const container = document.getElementById(containerId);
            if (container) {
                container.innerHTML = alertHtml;
            } else {
                console.error(`Container com ID "${containerId}" não encontrado.`);
            }
        } else {
            // Adiciona diretamente ao body
            const body = document.body;
            const alertElement = document.createElement('div');
            alertElement.innerHTML = alertHtml;

            // Adiciona o alert ao body
            body.appendChild(alertElement.firstElementChild);

            // Remove automaticamente após 5 segundos
            setTimeout(() => {
                alertElement.firstElementChild.classList.remove('show');
                alertElement.firstElementChild.addEventListener('transitionend', () => {
                    alertElement.remove();
                });
            }, 5000);
        }
    }
}


const createLoader = (() => {
    let modalElement;

    // Cria o modal dinamicamente
    const createModal = () => {
        const modalHTML = `
        <div 
          id="loader-modal" 
          class="d-flex justify-content-center align-items-center position-fixed w-100 h-100" 
          style="top: 0; left: 0; background: rgba(0, 0, 0, 0.5); z-index: 1050; cursor: wait;">
          <div class="spinner-border text-light" role="status" style="width: 3rem; height: 3rem;">
            <span class="sr-only">Loading...</span>
          </div>
        </div>
      `;

        // Insere no body
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        modalElement = document.getElementById('loader-modal');
    };

    // Exibe o loader
    const showLoader = () => {
        if (!modalElement) createModal();
        modalElement.style.display = 'flex'; // Certifica-se de exibir o loader
        document.body.style.cursor = 'wait'; // Define o cursor como loader
    };

    // Oculta e remove o loader
    const hideLoader = () => {
        if (modalElement) {
            modalElement.remove(); // Remove o modal do DOM
            modalElement = null; // Limpa a referência
        }
        document.body.style.cursor = 'default'; // Restaura o cursor padrão
    };

    // Retorna os métodos públicos
    return {
        show: showLoader,
        hide: hideLoader,
    };
});

function togglePasswordFields() {
    // Remove a classe que controla a visibilidade dos campos
    const passwordDiv = document.getElementById('passworddiv');
    const newPasswordDiv = document.getElementById('newpassworddiv');
    const newPasswordConfirmDiv = document.getElementById('newpasswordconfirmdiv');
    const passwordButton = document.getElementById('passwordButton')

    const passwordInput = document.getElementById('password');
    const newPasswordInput = document.getElementById('newpassword');
    const passwordConfirmInput = document.getElementById('passwordconfirm');

    // Remove a classe 'display-tags' que controla a visibilidade
    passwordDiv.classList.toggle('display-tags');
    newPasswordDiv.classList.toggle('display-tags');
    newPasswordConfirmDiv.classList.toggle('display-tags');

    // Adiciona a classe que controla a visibilidade
    passwordButton.classList.add("display-tags");

    // Verifica se os campos estão visíveis (a classe 'display-tags' foi removida)
    const areFieldsVisible = !passwordDiv.classList.contains('display-tags');

    // Se os campos estiverem visíveis, define os campos como 'required'
    if (areFieldsVisible) {
        passwordInput.required = true;
        newPasswordInput.required = true;
        passwordConfirmInput.required = true;
    } else {
        passwordInput.required = false;
        newPasswordInput.required = false;
        passwordConfirmInput.required = false;
    }
}