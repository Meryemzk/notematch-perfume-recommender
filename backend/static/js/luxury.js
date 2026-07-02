(function(){
  const topBtn=document.getElementById('backToTop');
  window.addEventListener('scroll',()=>{ if(topBtn) topBtn.classList.toggle('show', window.scrollY>500); });
  if(topBtn) topBtn.addEventListener('click',()=>window.scrollTo({top:0,behavior:'smooth'}));
  document.querySelectorAll('[data-loading]').forEach(btn=>btn.addEventListener('click',()=>{btn.classList.add('is-loading');}));
  document.querySelectorAll('.nm-filter-toggle').forEach(btn=>btn.addEventListener('click',()=>document.body.classList.toggle('filters-open')));
})();
