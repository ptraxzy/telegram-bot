
// Smooth nav active state & year
document.getElementById('year').textContent = new Date().getFullYear();

// Intersection Observer for scroll reveal
const io = new IntersectionObserver((entries)=>{
  entries.forEach(e=>{
    if(e.isIntersecting){
      e.target.classList.add('visible');
      io.unobserve(e.target);
    }
  });
},{threshold:.15});

document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

// Optional: highlight active nav link while scrolling
const sections = [...document.querySelectorAll('section[id]')];
const navLinks = [...document.querySelectorAll('.nav-link')];
function setActiveLink(){
  const y = window.scrollY + 120;
  let id = sections[0].id;
  sections.forEach(sec=>{ if(y >= sec.offsetTop) id = sec.id; });
  navLinks.forEach(a=>{
    a.classList.toggle('active', a.getAttribute('href') === '#' + id);
  });
}
window.addEventListener('scroll', setActiveLink);
setActiveLink();

// CSS class for active nav
const style = document.createElement('style');
style.textContent = `.nav-link.active{color: var(--bg);}`;
document.head.appendChild(style);
