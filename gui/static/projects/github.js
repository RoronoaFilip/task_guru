const folderIcon = (name) => `<i class="fa-regular fa-folder icon-text">${name}</i>`;
const fileIcon = (name) => `<i class="fa-regular fa-file icon-text">${name}</i>`;
const githubDiv = document.getElementById('github-structure');

setUpGithubDiv(url, githubDiv);

function setUpGithubDiv(url, div) {
    fetchUrl(url)
        .then(data => {
            data.filter(item => item.type === 'dir').forEach(dir => {
                createDir(div, dir, url);
            });
            data.filter(item => item.type === 'file').forEach(file => {
                createFile(div, file);
            });
        });
}

function createDir(parent, dir, url) {
    const button = document.createElement('button');

    button.clickedFlag = false;
    button.innerHTML = folderIcon(dir.name);
    button.classList.add('github-dir');
    addSpaceLeft(parent, button);
    parent.appendChild(button);

    const currUrl = url + '/' + dir.name;
    button.addEventListener('click', (event) => {
        event.preventDefault();
        event.stopPropagation();
        if (button.clickedFlag) {
            Array.from(button.children).slice(1).forEach(child => {
                button.removeChild(child);
            });
            button.clickedFlag = false;
        } else {
            setUpGithubDiv(currUrl, button);
            button.clickedFlag = true;
        }
    });
}

function createFile(parent, file) {
    const button = document.createElement('button');

    button.innerHTML = fileIcon(file.name);
    button.classList.add('github-file');
    button.disabled = true;
    addSpaceLeft(parent, button);
    parent.appendChild(button);
}

function addSpaceLeft(parent, element) {
    const currentLeft = +parent.style.left.match(/[\d.]+/);
    const newLeft = currentLeft + 30;
    element.style.left = `${newLeft}px`;
}

function fetchUrl(url) {
    return fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer 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'
        }
    })
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
