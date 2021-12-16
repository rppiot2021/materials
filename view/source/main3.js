import r from '@hat-open/renderer';

function main() {
    const rootElement = document.body.appendChild(document.createElement('div'))
    r.init(rootElement, { counter: 0 }, generateVirtualTree);
}


function generateVirtualTree() {
    return ['div',
        ['label', `${r.get('counter')}`],
        ['button', {
            on: {
                click: () => r.set(['counter'], r.get('counter') + 1)
            }},
            'Add'
        ],
        ['button', {
            on: {
                click: () => r.set(['counter'], 0)
            }},
            'Reset'
        ]
    ];
}


window.addEventListener('load', main);
window.r = r;
