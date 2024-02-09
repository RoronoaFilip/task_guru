const githubProxyUrl = 'http://localhost:8000/api/github/proxy';

const folderIcon = (githubFile) =>
    `<a class="fa-regular fa-folder github-element-wrapper icon-text" href="${githubFile.html_url}" target="_blank">
        <p class="icon-text name">${githubFile.name}</p>
    </a>`;

const fileIcon = (githubFile) =>
    `<a class="fa-regular fa-file github-element-wrapper icon-text file" href="${githubFile.html_url}" target="_blank">
        <p class="icon-text name file">${githubFile.name}</p>
    </a>`;

const githubDiv = document.getElementById('github-structure');

setUpGithubDiv(url, githubDiv);

function setUpGithubDiv(url, div) {
    fetchUrl(url)
        .then(data => {
            data.filter(item => item.type === 'dir').forEach(dir => {
                createDir(div, dir);
            });
            data.filter(item => item.type === 'file').forEach(file => {
                createFile(div, file);
            });
        });
}

function createDir(parent, dir) {
    const button = document.createElement('button');

    button.innerHTML = folderIcon(dir);
    button.classList.add('github-dir');
    addSpaceLeft(parent, button);
    parent.appendChild(button);

    const folder = button.firstChild;
    folder.clickedFlag = false;

    folder.addEventListener('click', (event) => {
        event.preventDefault();
        event.stopPropagation();
        if (folder.clickedFlag) {
            Array.from(button.children).slice(1).forEach(child => {
                button.removeChild(child);
            });
            folder.clickedFlag = false;
        } else {
            setUpGithubDiv(dir.url, button);
            folder.clickedFlag = true;
        }
    });
}

function createFile(parent, file) {
    const button = document.createElement('button');

    button.innerHTML = fileIcon(file);
    button.classList.add('github-file');
    button.disabled = true;
    addSpaceLeft(parent, button);
    parent.appendChild(button);
}

function addSpaceLeft(parent, element) {
    const currentLeft = +parent.style.left.match(/[\d.]+/);
    const newLeft = currentLeft + 20;
    element.style.left = `${newLeft}px`;
}

function fetchUrl(url) {
    return fetch(`${githubProxyUrl}?url=${url}`)
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Loading Github Structure Failed!');
        })
        .then(data => {
            return data;
        })
        .catch(error => {
            alert(error);
        });

}
