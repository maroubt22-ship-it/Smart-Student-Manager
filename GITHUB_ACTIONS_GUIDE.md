# GitHub Actions - Documentation

## 📁 Fichier créé
`.github/workflows/docker.yml`

---

## 🎯 Qu'est-ce que ce workflow fait?

### ✅ Automatisations incluses:

1. **Build Docker** 🐳
   - Construit l'image Docker automatiquement
   - Versioning avec tags Git
   - Timestamps pour tracking

2. **Tests** 🧪
   - Teste les imports (Flask, SQLAlchemy)
   - Vérifie la syntaxe Python
   - Valide le Dockerfile

3. **Qualité du code** 📊
   - Pylint check
   - Flake8 linting
   - Syntax validation

4. **Notifications** 📢
   - Affiche l'état du build
   - Resume les résultats

---

## 🚀 Configuration requise

### 1. Initialiser Git (si pas encore fait)
```bash
cd "C:\Users\pc\Desktop\Smart Student Manager"
git init
git add .
git commit -m "Initial commit"
```

### 2. Ajouter le remote GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/Smart-Student-Manager.git
git branch -M main
git push -u origin main
```

### 3. Créer les tags Git (optionnel)
```bash
git tag v1.0.0
git push origin v1.0.0
```

---

## 📋 Quand le workflow s'exécute?

**Automatiquement déclenché par:**

✅ Push sur `main`, `master`, ou `develop`
✅ Changements dans:
  - `app.py`
  - `requirements.txt`
  - `Dockerfile`
  - `templates/**`
  - `static/**`
  - `.github/workflows/docker.yml`

✅ Pull Request vers `main` ou `master`
✅ Déclenchement manuel (workflow_dispatch)

---

## 🔧 Options avancées

### Activer le push Docker Hub

Pour publier automatiquement vers Docker Hub:

#### 1. Ajouter les secrets GitHub

Aller à: **Settings → Secrets and variables → Actions**

Ajouter:
- `DOCKER_HUB_USERNAME`: Votre username Docker Hub
- `DOCKER_HUB_TOKEN`: Votre token Docker Hub

#### 2. Décommenter dans le workflow

Dans `.github/workflows/docker.yml`, décommenter:

```yaml
- name: Log in to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKER_HUB_USERNAME }}
    password: ${{ secrets.DOCKER_HUB_TOKEN }}

- name: Push to Docker Hub
  uses: docker/build-push-action@v5
  with:
    context: .
    file: ./Dockerfile
    push: true
    tags: |
      ${{ secrets.DOCKER_HUB_USERNAME }}/${{ env.IMAGE_NAME }}:${{ steps.version.outputs.VERSION }}
      ${{ secrets.DOCKER_HUB_USERNAME }}/${{ env.IMAGE_NAME }}:${{ steps.version.outputs.BUILD_ID }}
      ${{ secrets.DOCKER_HUB_USERNAME }}/${{ env.IMAGE_NAME }}:latest
```

---

## 📊 Voir les résultats

### Sur GitHub:

1. Aller à: **Actions** (tab dans ton repo)
2. Cliquer sur le workflow qui s'exécute
3. Voir les logs en temps réel

### Exemple de résultat:

```
✅ Checkout code
✅ Set up Docker Buildx
✅ Build Docker image
✅ Load image for testing
✅ Run container tests
   - Flask and SQLAlchemy imports successful
   - Flask app syntax check passed
✅ Code Quality Check
✅ Build Notification
```

---

## 🎨 Personnalisations possibles

### 1. Ajouter pytest pour les tests

```yaml
- name: Run tests
  run: |
    pip install pytest
    pytest tests/
```

### 2. Ajouter des checks de sécurité

```yaml
- name: Security scan
  run: |
    pip install bandit
    bandit -r app.py
```

### 3. Ajouter des notifs Slack/Discord

```yaml
- name: Notify Slack
  uses: slackapi/slack-github-action@v1.24.0
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "Build completed: ${{ job.status }}"
      }
```

### 4. Déployer automatiquement

```yaml
- name: Deploy to server
  run: |
    ssh user@server 'cd /app && docker-compose pull && docker-compose up -d'
```

---

## 🔐 Bonnes pratiques de sécurité

### ✅ À faire:
- Utiliser des secrets pour les credentials
- Limiter les permissions du token
- Vérifier les logs avant production
- Tester en develop avant main

### ❌ À éviter:
- Ne jamais commiter de credentials
- Ne pas pousser les `.env` files
- Éviter les secrets en plaintext dans le code

---

## 📝 Exemple complet avec Docker Hub

Voici un exemple d'utilisation complète:

```bash
# 1. Configuration initiale
git remote add origin https://github.com/votreuser/Smart-Student-Manager.git
git branch -M main

# 2. Ajouter le workflow (.github/workflows/docker.yml déjà créé)

# 3. Ajouter secrets sur GitHub (Settings → Secrets)
# DOCKER_HUB_USERNAME
# DOCKER_HUB_TOKEN

# 4. Faire un changement et pousser
echo "# Update" >> README.md
git add .
git commit -m "Update README"
git push -u origin main

# 5. GitHub Actions déclenche automatiquement!
# - Build l'image
# - Teste l'image
# - Pousse vers Docker Hub
# - Affiche les résultats
```

---

## 🐛 Troubleshooting

### Le workflow ne s'exécute pas?

```bash
# 1. Vérifier que le fichier existe
ls -la .github/workflows/docker.yml

# 2. Vérifier la syntaxe YAML
# Utiliser: https://yamllint.com/

# 3. Vérifier les permissions du repo
# Settings → Actions → General → Workflow permissions
```

### Build échoue?

```bash
# 1. Vérifier les logs GitHub
# Actions → Workflow → Voir les logs

# 2. Tester localement
docker build -t smart-student-manager .

# 3. Vérifier requirements.txt
pip install -r requirements.txt
```

### Docker Hub push ne fonctionne pas?

```bash
# 1. Vérifier les secrets sont ajoutés
# Settings → Secrets → Voir les secrets

# 2. Vérifier le token Docker Hub est valide
# Docker Hub → Account → Security → Tokens

# 3. Vérifier la ligne 'push: true' est décommentée
```

---

## ✨ Résumé

Ton workflow GitHub Actions:

✅ **Build automatique** - À chaque push
✅ **Tests intégrés** - Valide le code
✅ **Quality checks** - Pylint + Flake8
✅ **Versioning** - Tags automatiques
✅ **Optional push** - Vers Docker Hub
✅ **Notifications** - État du build
✅ **Professionnel** - Prêt pour production

**Prochaine étape:** Commiter et pousser vers GitHub!

```bash
git add .
git commit -m "Add GitHub Actions CI/CD workflow"
git push origin main
```

Puis regarde l'onglet **Actions** sur GitHub! 🚀
