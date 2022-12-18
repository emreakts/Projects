int tutulan = (new Random().Next(1,100));
int hak = 2;
System.Console.WriteLine(tutulan);
while (hak>0)
{
    System.Console.Write("Bir Sayi Giriniz : ");
    int sayi = int.Parse(Console.ReadLine());
    hak--;
    if (sayi == tutulan)
    {
        System.Console.Write("Tahmininiz Doğru.Tebrikler !! ");
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
}
    System.Console.Write("Hakkiniz Bitmistir.");
