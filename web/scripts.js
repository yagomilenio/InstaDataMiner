const cy = cytoscape({
    container: document.getElementById('cy'),

    elements: [
        // Nodos
        { data: { id: 'A', nombre: 'julio' } },
        { data: { id: 'B' } },
        { data: { id: 'C' } },
        { data: { id: 'D' } },
        { data: { id: 'E' } },
        { data: { id: 'F' } },
        { data: { id: 'G' } },
        { data: { id: 'H' } },
        { data: { id: 'I' } },
        { data: { id: 'J' } },

        // Aristas (conexiones)
        { data: { id: 'AB', source: 'A', target: 'B' } },
        { data: { id: 'AC', source: 'A', target: 'C' } },
        { data: { id: 'BD', source: 'B', target: 'D' } },
        { data: { id: 'CE', source: 'C', target: 'E' } },
        { data: { id: 'DF', source: 'D', target: 'F' } },
        { data: { id: 'EF', source: 'E', target: 'F' } },
        { data: { id: 'FG', source: 'F', target: 'G' } },
        { data: { id: 'GH', source: 'G', target: 'H' } },
        { data: { id: 'HI', source: 'H', target: 'I' } },
        { data: { id: 'IJ', source: 'I', target: 'J' } },
        { data: { id: 'AJ', source: 'A', target: 'J' } },
        { data: { id: 'CH', source: 'C', target: 'H' } },
        { data: { id: 'DE', source: 'D', target: 'E' } },
        { data: { id: 'BG', source: 'B', target: 'G' } }
    ]
    ,

    style: [
        {
            selector: 'node',
            style: {
                'background-color': '#666',
                'label': 'data(id)',
                'color': 'white',
                'text-valign': 'center',
                'text-halign': 'center'
            }
        },
        {
            selector: 'edge',
            style: {
                'width': 3,
                'line-color': '#ccc'
            }
        }
    ],

    layout: {
        name: 'grid'
    }
});