#!/bin/sh
# POSIX-safe; no bashisms. Handles spaces and apostrophes in paths.

set -eu

# --- arg parse ---
TCGA_GZ=""
SUPP_IN=""
TCGA_OUT=""
SUPP_OUT=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --tcga-gz)  TCGA_GZ=$2;  shift 2 ;;
    --supp)     SUPP_IN=$2;  shift 2 ;;
    --tcga-out) TCGA_OUT=$2; shift 2 ;;
    --supp-out) SUPP_OUT=$2; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

# --- sanity ---
[ -n "$TCGA_GZ" ]  || { echo "TCGA .gz path missing"; exit 2; }
[ -n "$SUPP_IN" ]  || { echo "Supplemental path missing"; exit 2; }
[ -n "$TCGA_OUT" ] || { echo "TCGA out dir missing"; exit 2; }
[ -n "$SUPP_OUT" ] || { echo "Supp out dir missing"; exit 2; }

# Normalize dirs exist
mkdir -p "$TCGA_OUT" "$SUPP_OUT"

# --- TCGA copy + optional extract ---
tcga_base="tcga_RSEM_gene_tpm.gz"
tcga_dst_gz="$TCGA_OUT/$tcga_base"
cp "$TCGA_GZ" "$tcga_dst_gz"
echo "✅ TCGA → $tcga_dst_gz"

# try to extract to .tsv next to it (do not fail pipeline if gzip can’t read)
if command -v gunzip >/dev/null 2>&1; then
  if gunzip -c "$tcga_dst_gz" >/dev/null 2>&1; then
    gunzip -c "$tcga_dst_gz" > "$TCGA_OUT/tcga_RSEM_gene_tpm.tsv"
    echo "✅ Extracted TSV → $TCGA_OUT/tcga_RSEM_gene_tpm.tsv"
  else
    echo "ℹ️  Gzip not extractable; kept .gz only."
  fi
else
  echo "ℹ️  gunzip not found; kept .gz only."
fi

# --- Supplemental copy (keep original filename) ---
supp_name=$(basename -- "$SUPP_IN")
cp "$SUPP_IN" "$SUPP_OUT/$supp_name"
echo "✅ Supplemental → $SUPP_OUT/$supp_name"