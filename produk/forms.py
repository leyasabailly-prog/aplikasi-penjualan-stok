from django import forms
from .models import Produk


class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = [
            'kode_produk', 'nama_produk', 'kategori', 'supplier',
            'harga_beli', 'harga_jual', 'stok', 'stok_minimum',
            'satuan', 'gambar', 'is_active',
        ]
        widgets = {
            'kode_produk': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'PRD002'}),
            'nama_produk': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nama produk'}),
            'kategori': forms.Select(attrs={'class': 'form-input'}),
            'supplier': forms.Select(attrs={'class': 'form-input'}),
            'harga_beli': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'harga_jual': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'stok': forms.NumberInput(attrs={'class': 'form-input'}),
            'stok_minimum': forms.NumberInput(attrs={'class': 'form-input'}),
            'satuan': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'pcs / kg / dus'}),
            'gambar': forms.ClearableFileInput(attrs={'class': 'form-input-file'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        harga_beli = cleaned_data.get('harga_beli')
        harga_jual = cleaned_data.get('harga_jual')
        if harga_beli is not None and harga_jual is not None and harga_jual < harga_beli:
            raise forms.ValidationError('Harga jual tidak boleh lebih kecil dari harga beli.')
        return cleaned_data