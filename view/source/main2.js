import r from '@hat-open/renderer';

function main() {
    const rootElement = document.body.appendChild(document.createElement('div'))
    r.init(rootElement, {}, generateVirtualTree);
}


function generateVirtualTree() {
    return ['div', 'generated by the renderer'];
}


window.addEventListener('load', main);
window.r = r;