import subprocess
import sys

def is_service_running(service_name):
    result = subprocess.run(['sc', 'query', service_name], capture_output=True, text=True)
    return 'RUNNING' in result.stdout

def check_event_log():
    print(f"Checking event viewer...\n")
    powershell_cmd = """
    Get-WinEvent -LogName "Microsoft-Windows-Windows Defender/Operational" | 
    Where-Object { $_.Id -eq 5007 } |
    Select-Object -ExpandProperty Message
    """
    result = subprocess.run(['powershell', '-Command', powershell_cmd], capture_output=True, text=True)
    if result.stdout:
        search_string = "New value: HKLM\\SOFTWARE\\Microsoft\\Windows Defender\\Exclusions\\Paths\\"
        for line in result.stdout.split('\n'):
            index = line.find(search_string)
            if index != -1:
                path = line[index + len(search_string):].split('=')[0]
                print(f"[+] {path}")

def main():
    if not is_service_running("WinDefend"):
        print(f"Windows Defender is not running.")
        sys.exit()
    else:
        print(f"Windows Defender is running.")
        check_event_log()

if __name__ == "__main__":
    main()
