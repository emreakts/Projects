Console.Write("Adet Sayisi Giriniz :");
 int adet = int.Parse(Console.ReadLine());

string[] urunler = new string[adet];

 int i = 0 ;
 do
 {
    Console.Write($" {i+1}. Ürün Adı Giriniz : ");
    urunler[i] = Console.ReadLine();
    i++;
 } while (adet!=i);

Console.WriteLine(" Ürünler Listeleniyor ...");

for (int a = 0; a < urunler.Length; a++)
{
Console.WriteLine($" {a+1}. Ürün Adı : {urunler[a]}" );
}
