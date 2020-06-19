
<script>
    const btnOpen{{ ansible_hostname  | regex_replace('-','_')}} = document.querySelector('#Open-{{ ansible_hostname  | regex_replace('-','_')}}'),
    Table{{ ansible_hostname  | regex_replace('-','_')}} = document.querySelector('#Table-{{ ansible_hostname  | regex_replace('-','_')}}');
    btnOpen{{ ansible_hostname  | regex_replace('-','_')}}.addEventListener('click',() => {
        $('.tabla').each(function() {
            if ( $(this).hasClass("Table-{{ ansible_hostname  | regex_replace('-','_')}}") ) {
                Table{{ ansible_hostname  | regex_replace('-','_')}}.classList.toggle('active');
                $(this).css('display', 'table');
            }else{
                $(this).removeClass('active');
                $(this).css('display', 'none');
            }
        });
    });
</script>
