do {
int tutulan = (new Random().Next(1,100));
int hak = 5;
int tur=0;
double sp = 100/hak;

System.Console.WriteLine(tutulan);
while (hak>0)
{
    tur++;
    System.Console.WriteLine($"{tur}. Deneme");
    System.Console.Write("Bir Sayi Giriniz : ");
    int sayi = int.Parse(Console.ReadLine());
    hak--;
    if (sayi == tutulan)
    {
        double puan = 100-(sp*(tur-1));
        System.Console.WriteLine($"{tur}. Denemede Tahmininiz Doğru Tebrikler !! ");
        System.Console.WriteLine($"Kazanilan Puan {puan}");
        break;
    }
    else
        {
        if (hak==0)
        break;
        if (tutulan>sayi)
            System.Console.WriteLine("Daha Büyük Sayi Tahmin Ediniz ");    
        else
             System.Console.WriteLine("Daha Düşük Sayi Tahmin Ediniz ");
        }    
}       System.Console.WriteLine("Hakkiniz Bitmistir.");
        System.Console.Write(" Devam Etmek istiyor musunuz ? (e/h) : ");

        string result = Console.ReadLine();

                if (result=="h" || result =="hayır")
                    break;
  }  while (true) ;
    
