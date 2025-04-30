document.addEventListener('DOMContentLoaded', function() {
    const downloadBtn = document.getElementById('download-png');

    if(downloadBtn) {
        downloadBtn.addEventListener('click', async function() {
            
            const element = document.getElementById('content');

            if(!element) {
                console.error('#content element does not exist');
                return;
            }

            try {
                const canvas = await html2canvas(element);
                
                // convertir le canvas en image
                const image = canvas.toDataURL('image/png');
    
                // créer un lien de téléchargement
                const link = document.createElement('a');
                link.href = image;
                link.download = 'eMatrix_tasks_' + new Date().toISOString().slice(0, 10) + '.png';
    
                // déclencher le téléchargement
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                
            } catch(error) {
                console.error('An Error occurred during the shot: ', error);
                alert('This service is temporarily unavailable');
            }
        });
    }
});