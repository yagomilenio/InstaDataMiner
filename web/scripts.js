document.getElementById('fileInput').addEventListener('change', e => {
    const file = e.target.files[0];
    if (!file) return;

    Papa.parse(file, {
        header: true,
        skipEmptyLines: true,
        complete: results => {
            console.log("Datos CSV:", results.data);
            const elementos=[];
            const data = results.data
            data.forEach((fila, index) => {
                console.log(fila)
                for (const clave in fila) {

                    elementos.push({data:{id: `${clave}`}})
                }
            });

            data.forEach((fila, index) => {
                console.log(fila)
                for (const clave in fila) {

                    elementos.push({data:{id: `${fila[clave]}`}})
                }
            });


            data.forEach((fila, index) => {
                console.log(fila)
                for (const clave in fila) {
                    console.log(`  ${clave}: ${fila[clave]}`);
                    elementos.push({data:{id: `${clave}${fila[clave]}`, source: `${clave}`, target:`${fila[clave]}`}})
                }
            });

            document.getElementById('fileInput').style.display = 'none';

            const cy = cytoscape({
                container: document.getElementById('cy'),

                elements: elementos,

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

        },
        error: err => {
            console.error("Error leyendo CSV:", err);
        }
    });
});


