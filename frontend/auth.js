const authScreen=document.querySelector('#auth-screen'),authForm=document.querySelector('#auth-form'),authError=document.querySelector('#auth-error'),authLabel=document.querySelector('#auth-submit-label');let authMode='signin';
document.querySelectorAll('.auth-tab').forEach(tab=>tab.onclick=()=>{authMode=tab.dataset.authTab;document.querySelectorAll('.auth-tab').forEach(x=>x.classList.toggle('active',x===tab));authLabel.textContent=authMode==='signin'?'Sign In':'Create Account';authError.textContent=''});
document.querySelector('#toggle-password').onclick=()=>{const input=document.querySelector('#auth-password');input.type=input.type==='password'?'text':'password'};
document.querySelector('#auth-close').onclick=()=>authScreen.classList.add('hidden');
authForm.onsubmit=e=>{e.preventDefault();if(!authForm.checkValidity()){authError.textContent='Use a valid email and a password with at least 12 characters.';return}sessionStorage.setItem('job-tracker-authenticated','true');authScreen.classList.add('hidden')};
if(sessionStorage.getItem('job-tracker-authenticated')==='true')authScreen.classList.add('hidden');
