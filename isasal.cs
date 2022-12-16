Console.WriteLine(" **** 22.Ders_uygulama **** ");

bool isasal = true ;

System.Console.Write(" Bir Sayi Giriniz : ");
int sayi =int.Parse(System.Console.ReadLine());

if (sayi==1)
{ isasal=false;
    System.Console.WriteLine(" Sayi Asal");
}

for (int i = 2; i < sayi; i++)
{
    if(sayi%i==0){
        isasal=false;
        System.Console.WriteLine("Sayi Asal Değildir");
        break;
    }
}
    if (isasal)
    {
        System.Console.WriteLine("Sayi Asaldır");
    }