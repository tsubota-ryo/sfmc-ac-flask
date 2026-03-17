"""全ドキュメントを目次付きPDFに統合するスクリプト"""
import markdown
from weasyprint import HTML
import os

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))

# ドキュメントの順序と表示名
DOC_FILES = [
    ("overview.md", "1. プロジェクト概要"),
    ("api-reference.md", "2. API リファレンス"),
    ("models.md", "3. モデル定義"),
    ("frontend.md", "4. フロントエンド仕様"),
    ("config-json-spec.md", "5. config.json 仕様書"),
    ("setup-and-deployment.md", "6. セットアップ・デプロイガイド"),
]

def read_md(filename):
    with open(os.path.join(DOCS_DIR, filename), "r", encoding="utf-8") as f:
        return f.read()

def build_toc_html():
    items = ""
    for filename, title in DOC_FILES:
        anchor = filename.replace(".md", "")
        items += f'<li><a href="#{anchor}">{title}</a></li>\n'
    return f"""
    <div class="toc">
        <h2>目次</h2>
        <ol>{items}</ol>
    </div>
    <div style="page-break-after: always;"></div>
    """

def build_full_html():
    md_ext = ["tables", "fenced_code", "codehilite", "toc", "nl2br"]
    toc = build_toc_html()
    sections = ""
    for filename, title in DOC_FILES:
        anchor = filename.replace(".md", "")
        md_content = read_md(filename)
        html_body = markdown.markdown(md_content, extensions=md_ext)
        sections += f'<section id="{anchor}">{html_body}</section>\n'
        sections += '<div style="page-break-after: always;"></div>\n'

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<style>
@page {{
    size: A4;
    margin: 20mm 15mm 20mm 15mm;
    @bottom-center {{
        content: counter(page);
        font-size: 10px;
        color: #666;
    }}
}}
body {{
    font-family: "Hiragino Kaku Gothic ProN", "Hiragino Sans", "Yu Gothic", "Meiryo", sans-serif;
    font-size: 11pt;
    line-height: 1.7;
    color: #222;
}}
h1 {{
    font-size: 22pt;
    color: #1a3a5c;
    border-bottom: 3px solid #1a3a5c;
    padding-bottom: 8px;
    margin-top: 0;
}}
h2 {{
    font-size: 16pt;
    color: #2a5a8c;
    border-bottom: 1px solid #ccc;
    padding-bottom: 5px;
    margin-top: 24px;
}}
h3 {{
    font-size: 13pt;
    color: #3a6a9c;
    margin-top: 20px;
}}
h4 {{
    font-size: 11pt;
    color: #4a7aac;
}}
table {{
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
    font-size: 10pt;
}}
th, td {{
    border: 1px solid #ccc;
    padding: 6px 10px;
    text-align: left;
}}
th {{
    background-color: #f0f4f8;
    font-weight: bold;
}}
tr:nth-child(even) {{
    background-color: #fafbfc;
}}
code {{
    background-color: #f4f4f4;
    padding: 1px 5px;
    border-radius: 3px;
    font-family: "SF Mono", "Monaco", "Menlo", "Consolas", monospace;
    font-size: 9.5pt;
}}
pre {{
    background-color: #f6f8fa;
    border: 1px solid #e1e4e8;
    border-radius: 6px;
    padding: 12px 16px;
    overflow-x: auto;
    font-size: 9pt;
    line-height: 1.5;
}}
pre code {{
    background-color: transparent;
    padding: 0;
}}
blockquote {{
    border-left: 4px solid #dfe2e5;
    padding: 8px 16px;
    margin: 12px 0;
    color: #555;
    background-color: #fafafa;
}}
a {{
    color: #0366d6;
    text-decoration: none;
}}
hr {{
    border: none;
    border-top: 1px solid #ddd;
    margin: 20px 0;
}}
/* 目次 */
.toc {{
    margin-top: 40px;
}}
.toc h2 {{
    font-size: 20pt;
    text-align: center;
    border-bottom: none;
}}
.toc ol {{
    font-size: 13pt;
    line-height: 2.2;
    max-width: 500px;
    margin: 20px auto;
}}
.toc a {{
    color: #1a3a5c;
}}
/* タイトルページ */
.cover {{
    text-align: center;
    padding-top: 180px;
}}
.cover h1 {{
    font-size: 28pt;
    border-bottom: none;
    color: #1a3a5c;
}}
.cover p {{
    font-size: 13pt;
    color: #666;
    margin-top: 20px;
}}
</style>
</head>
<body>
    <div class="cover">
        <h1>SFMC Custom Activity<br>Flask アプリケーション<br>技術ドキュメント</h1>
        <p>Version 1.0</p>
    </div>
    <div style="page-break-after: always;"></div>
    {toc}
    {sections}
</body>
</html>"""

if __name__ == "__main__":
    html_content = build_full_html()

    # HTML ファイルとして保存
    html_path = os.path.join(DOCS_DIR, "sfmc-ac-flask-documentation.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML generated: {html_path}")

    # PDF ファイルとして保存
    output_path = os.path.join(DOCS_DIR, "sfmc-ac-flask-documentation.pdf")
    HTML(string=html_content, base_url=DOCS_DIR).write_pdf(output_path)
    print(f"PDF generated: {output_path}")
