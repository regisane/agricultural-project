# 🚀 Deployment Checklist

**Project:** Agricultural Investment Risk Analysis  
**Version:** 2.0 Professional  
**Last Updated:** 2026-08-15

---

## ✅ Pre-Deployment Verification

### 1. Code Quality & Testing
- [ ] All Python files compile without errors
  ```bash
  python -m py_compile app.py agricultural_analysis.py cli.py config_template.py
  ```
- [ ] Requirements file is valid and tested
  ```bash
  pip install -r requirements.txt
  ```
- [ ] No hardcoded credentials or sensitive data in code
- [ ] All imports are available in `requirements.txt`
- [ ] Git status is clean
  ```bash
  git status
  ```

### 2. Data & Output Validation
- [ ] Input data file exists: `faostat_landuse.csv`
- [ ] Run full analysis locally and verify outputs
  ```bash
  python agricultural_analysis.py
  ```
- [ ] Check that all output files are generated:
  - [ ] `output/agricultural_master_data.csv`
  - [ ] `output/final_results.csv`
  - [ ] `output/analysis_summary.json`
  - [ ] `output/agricultural_analysis.png`
  - [ ] `output/spatial_analysis_map.png`
  - [ ] `output/interactive_risk_map.html`
  - [ ] `output/analysis.log`
- [ ] Verify output schema contains required columns
  ```bash
  python - <<'PY'
  import pandas as pd
  master = pd.read_csv('output/agricultural_master_data.csv')
  results = pd.read_csv('output/final_results.csv')
  required_master = ['Country','Investment_Score','Composite_Risk_Score','Agricultural_Land_1000ha']
  required_results = ['Longitude','Latitude','Predicted_Score']
  assert all(c in master.columns for c in required_master)
  assert all(c in results.columns for c in required_results)
  print('✅ All required columns present')
  PY
  ```
- [ ] File sizes are reasonable (not corrupted)
  ```bash
  ls -lh output/
  ```

### 3. Dashboard Testing
- [ ] Streamlit app starts without errors locally
  ```bash
  streamlit run app.py --server.headless true --server.port 8503
  ```
- [ ] All pages load and render correctly
  - [ ] 📈 Overview page (metrics & insights)
  - [ ] 🗺️ Geographic Analysis (filtering & maps)
  - [ ] 💰 Investment Metrics (distributions & rankings)
  - [ ] ⚠️ Risk Assessment (risk scores & categories)
  - [ ] 📊 Data Explorer (search & download)
  - [ ] 📉 Visualizations (heatmaps & comparisons)
  - [ ] ℹ️ About & Info (documentation & links)
- [ ] No KeyError or missing column errors
- [ ] Interactive features work (filters, search, download)
- [ ] Visualizations render without timeout
- [ ] HTTP response is 200 OK
  ```bash
  curl -I http://127.0.0.1:8503
  ```

### 4. Documentation & Configuration
- [ ] README.md is complete and up-to-date
- [ ] QUICK_REFERENCE.md contains correct commands
- [ ] STREAMLIT_GUIDE.md has deployment platform instructions
- [ ] LAUNCH_SUMMARY.md clearly explains what the app does
- [ ] All file paths in docs are relative and correct
- [ ] No broken links in markdown files
- [ ] `requirements.txt` has pinned versions for reproducibility

### 5. Git & Repository
- [ ] All changes are committed
  ```bash
  git status  # Should show "nothing to commit"
  ```
- [ ] Branch is set to `main`
  ```bash
  git branch  # Should show "* main"
  ```
- [ ] Latest commit includes all changes
  ```bash
  git log --oneline -5
  ```
- [ ] Repository is pushed to remote
  ```bash
  git push origin main --dry-run  # Check what would be pushed
  ```

---

## 🌐 Deployment Platform: Streamlit Cloud (Recommended)

### Setup Steps
1. **Create Account** at https://streamlit.io/cloud
2. **Connect GitHub**
   - Sign in with your GitHub account
   - Authorize Streamlit Cloud to access repositories
   - Link to `regisane/agricultural-project`

3. **Create New App**
   - Click "New app"
   - Select repository: `regisane/agricultural-project`
   - Set main file path: `app.py`
   - Choose Python version: 3.11+

4. **Configure Secrets** (if needed)
   - Go to Settings → Secrets
   - Add any environment variables (currently none required)

5. **Deploy**
   - Click "Deploy"
   - Wait for build to complete (~2-5 minutes)
   - Monitor logs for errors

### Post-Deployment Verification
- [ ] App loads at provided Streamlit URL
- [ ] Dashboard displays without "missing CSV" errors
- [ ] All pages load successfully
- [ ] Geographic map renders
- [ ] No Python errors in logs
- [ ] Performance is acceptable (~5s load time)

---

## 🔄 Other Deployment Options

### Docker (Self-Hosted)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

**Deployment:**
- [ ] Docker image builds successfully
- [ ] Container starts without errors
- [ ] Port 8501 (default Streamlit) is exposed
- [ ] Volume/persistent storage configured for output files

### Heroku
- [ ] Account created and connected to GitHub
- [ ] `Procfile` configured: `web: streamlit run app.py`
- [ ] Environment variables set (if needed)
- [ ] App deployed and running
- [ ] No "R14 (Memory exceeded)" errors

### AWS/Azure/GCP
- [ ] Infrastructure as Code (Terraform/CloudFormation) ready
- [ ] Virtual machine or container cluster provisioned
- [ ] Security groups/firewall rules configured
- [ ] SSL/TLS certificates installed
- [ ] Health checks configured
- [ ] Auto-scaling policies set (if applicable)

---

## 📊 Performance Benchmarks

### Expected Metrics (Streamlit Cloud)
- **Initial Load:** 2-5 seconds
- **Page Navigation:** <1 second
- **Data Operations:** <2 seconds
- **Chart Rendering:** <3 seconds
- **Interactive Map:** <5 seconds
- **Memory Usage:** <512 MB
- **CPU Usage:** <30% average

### Acceptable Ranges
✅ If deployment meets these metrics, you're good to go.  
⚠️ If any metric exceeds 2x the expected value, investigate.

---

## 🚨 Troubleshooting Deployment Issues

### Issue: "Missing CSV / Analysis not found"
**Solution:**
1. Verify `output/` directory exists and contains files
2. Check `app.py` has fallback logic to auto-generate via `agricultural_analysis.py`
3. Review logs for missing dependencies (pandas, geopandas, etc.)
4. Ensure `faostat_landuse.csv` is in repository root

### Issue: "ModuleNotFoundError"
**Solution:**
1. Verify all imports are in `requirements.txt`
2. Check package names match (e.g., `scikit-learn` not `sklearn`)
3. Ensure no local-only modules are being imported

### Issue: "Geospatial columns missing (Latitude/Longitude)"
**Solution:**
1. Confirm `agricultural_analysis.py` adds coordinates correctly
2. Verify `output/final_results.csv` contains these columns
3. Check that `app.py` guards against missing columns

### Issue: "App timeout or slow performance"
**Solution:**
1. Reduce data visualization complexity if streaming >500 countries
2. Use `st.cache_data` for expensive operations (already implemented)
3. Consider running analysis once and committing output files
4. Monitor memory usage in logs

### Issue: "Interactive map doesn't load"
**Solution:**
1. Verify `interactive_risk_map.html` is in repository root
2. Check Folium map generation in `agricultural_analysis.py`
3. Ensure browser supports WebGL (for map rendering)

---

## 📋 Final Sign-Off

Before deploying to production, confirm:

- [ ] **Code Quality:** All tests pass, no linting errors
- [ ] **Data Integrity:** All outputs generated correctly
- [ ] **Dashboard Stability:** All pages load without errors
- [ ] **Documentation:** Complete and accurate
- [ ] **Performance:** Meets acceptable benchmarks
- [ ] **Security:** No credentials in code or configs
- [ ] **Team Review:** Signed off by project owner
- [ ] **Backup:** Latest code is tagged for release
  ```bash
  git tag -a v2.0-production -m "Production release - 2026-08-15"
  git push origin v2.0-production
  ```

---

## 🎉 Deployment Complete!

After successful deployment:
1. ✅ Share live URL with stakeholders
2. ✅ Monitor logs for errors daily for first week
3. ✅ Gather user feedback and iterate
4. ✅ Plan next features/improvements
5. ✅ Keep `requirements.txt` updated for security patches

**Live URL:** `[Your Streamlit Cloud URL here]`  
**Deployed Date:** YYYY-MM-DD  
**Deployed By:** [Your Name]  
**Notes:** [Any special deployment considerations]

---

**Questions?** See `STREAMLIT_GUIDE.md` for deployment platform instructions or review `README.md` for general information.
