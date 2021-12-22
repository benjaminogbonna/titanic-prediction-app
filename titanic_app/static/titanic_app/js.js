let result = document.querySelector('p');
    if (result.textContent.includes('Survived')){
       result.classList.add('success');
    } else if(result.textContent.includes('Died')){
        result.classList.add('error');
    }