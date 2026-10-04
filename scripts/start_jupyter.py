"""Launch local Jupyter with session-only credentials inherited by notebook kernels."""
import os,sys,subprocess,getpass
if __name__=='__main__':
    env=dict(os.environ)
    live=input('Launch with approved live model access? [y/N] ').strip().lower()=='y'
    env['LIVE_MODE']='1' if live else '0'
    if live:
        for prefix in ['CHAT','EMBED']:
            env[prefix+'_URL']=input(prefix+' HTTPS base URL: ').strip()
            env[prefix+'_MODEL']=input(prefix+' exact model ID: ').strip()
            env[prefix+'_KEY']=getpass.getpass(prefix+' key (hidden): ')
        second=input('Optional second chat model ID, or Enter: ').strip()
        if second:env['CHAT_MODEL_B']=second
        options=input('Tested CHAT_OPTIONS JSON, or Enter for defaults: ').strip()
        if options:env['CHAT_OPTIONS']=options
    # Credentials are in this child process environment only; no credential file is written.
    raise SystemExit(subprocess.call([sys.executable,'-m','jupyterlab'],env=env))
