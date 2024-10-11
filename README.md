# RedSocialFinalG1-CTC

Red Social con Django

### Pasos para la instalación:

1. **Crear un entorno virtual (opcional pero recomendado):**
   Es una buena práctica crear un entorno virtual para cada proyecto Python. Esto ayuda a mantener las dependencias del proyecto separadas de otros proyectos y del sistema global. Para crear un entorno virtual, abre una terminal y ejecuta los siguientes comandos:

   ```bash
    python -m venv myenv
   ```

   Esto creará un nuevo directorio llamado `myenv` que contendrá el entorno virtual.

2. **Activar el entorno virtual:**

   ```bash
      .\env\Scripts\activate o
      source env/scripts/activate
   ```

   Esto activará el entorno virtual. Verás `(myenv)` en el prefijo de tu línea de comandos, lo que indica que el entorno virtual está activo.

3. **Instalar las librerías requeridas:**

   ```bash
   pip install -r requirements.txt
   ```

   Este comando instalará todas las librerías especificadas en la versión exacta indicada.

4. **Desactivar el entorno virtual (opcional):**
   Cuando hayas terminado de trabajar en tu proyecto, puedes desactivar el entorno virtual con el siguiente comando:
   `bash
    deactivate
    `
5. **Correr el servidor (opcional):**

   ```bash
   python manage.py runserver
   ```

6. **Ver las Mograciones en la DB(opcional):**
   ```bash
   python manage.py showmigrations
   ```
7. **Aplicar Mograciones pendientes en la DB(opcional):**
   ```bash
   python manage.py migrate
   ```
8. **Crear cambios de la DB (solo si cambias el modelo ) (opcional):**
   ```bash
   python manage.py makemigrations
   ```