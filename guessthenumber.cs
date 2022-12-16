Console.WriteLine(" **** 23.Ders **** ");

int tutulan = (new Random().Next(1,10));
int hak = 5;
while (hak>0)
{
    System.Console.WriteLine("Bir Sayi Giriniz : ");
    int sayi = int.Parse(Console.ReadLine());
    if (sayi == tutulan)
    {
        System.Console.WriteLine("Tahmininiz Doğru.Tebrikler !! ");
        break;
    }
    else
        {
        System.Console.WriteLine(" Tekrar Deneyiniz ");
        if (tutulan>sayi)
            System.Console.WriteLine("Daha Büyük Sayi Tahmin Ediniz :");    
        else
             System.Console.WriteLine("Daha Düşük Sayi Tahmin Ediniz : ");
        }
        hak--;
}
    
