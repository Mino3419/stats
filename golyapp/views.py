from django.shortcuts import render
from .models import Stats, ROK, CLUB, Logo
from django.db.models import Sum, Avg




def index(request):
    stati=Stats.objects.values("id_player","meno","pozicia").annotate(
        sumazapasov=Sum("zapasy"),
        sumagolov=Sum("g"),
        sumaasistencií=Sum("a"),
        sumabodov=Sum("b"),
        sumaplus=Sum("plusminus"),
        sumav=Sum("v"),
        sumagvp=Sum("gvp"),
        sumagvo=Sum("gvo"),
        sumav_g=Sum("v_g"),
        sumagvot=Sum("gvot"),
        sumastrely=Sum("strely"),
        priemerperc=Avg("perc_strel"),
        priemerbuly=Avg("buly"),

    ).order_by("-sumabodov")
    return render(request,"golyapp/index.html",{"stati":stati})

def pdetail(request,ide):
    stat=Stats.objects.filter(id_player=ide).order_by("sezona")
    hrac=stat.first()
    sumar=stat.aggregate(
        szapasy=Sum("zapasy"),
        sg=Sum("g"),
        sa=Sum("a"),
        sb=Sum("b"),
        splusminus=Sum("plusminus"),
        sv=Sum("v"),
        sgvp=Sum("gvp"),
        sgvo=Sum("gvo"),
        sv_g=Sum("v_g"),
        sgvot=Sum("gvot"),
        sstrely=Sum("strely"),
        aperc_strel=Avg("perc_strel"),
        abuly=Avg("buly")
                        )
    udaje=ROK.objects.get(id_player=ide)
    return render(request,"golyapp/detail.html",{
        "stat":stat,
        "hrac":hrac,
        "sumar":sumar,
        "udaje":udaje

                                                 }
                  )

def archiv(request):
    vsetky_sezony=Stats.objects.values_list("sezona",flat=True).distinct().order_by("-sezona")
    aktualna_sezona=vsetky_sezony[0] if vsetky_sezony else None
    zvolena_sezona=request.POST.get("vf",aktualna_sezona)
    stati=[]
    if zvolena_sezona:
        stati=Stats.objects.filter(sezona=zvolena_sezona).values(
            "id_player", 
            "meno", 
            "pozicia"
        ).annotate(
        sumazapasov=Sum("zapasy",distinct=True),
        sumagolov=Sum("g",distinct=True),
        sumaasistencií=Sum("a",distinct=True),
        sumabodov=Sum("b",distinct=True),
        sumaplus=Sum("plusminus",distinct=True),
        sumav=Sum("v",distinct=True),
        sumagvp=Sum("gvp",distinct=True),
        sumagvo=Sum("gvo",distinct=True),
        sumav_g=Sum("v_g",distinct=True),
        sumagvot=Sum("gvot",distinct=True),
        sumastrely=Sum("strely",distinct=True),
        priemerperc=Avg("perc_strel"),
        priemerbuly=Avg("buly"),
       
       
    ).order_by("-sumabodov","zapasy","-g")

    return render(request,"golyapp/archiv.html",{
            "sta":stati,
            "sezony":vsetky_sezony,
            "vybrata":zvolena_sezona

                                                     })
def slovak(request):
    nation_list=ROK.objects.values_list("krajina_nar",flat=True).distinct().order_by("krajina_nar")
    zvoleny_nar=request.POST.get("narod","SVK")
    nations=ROK.objects.filter(krajina_nar=zvoleny_nar).values_list("id_player",flat=True)
    stati=Stats.objects.filter(id_player__in=nations).values("id_player","meno","pozicia").annotate(
        szapasy=Sum("zapasy"),
        sg=Sum("g"),
        sa=Sum("a"),
        sb=Sum("b"),
        splusminus=Sum("plusminus"),
        sv=Sum("v"),
        sgvp=Sum("gvp"),
        sgvo=Sum("gvo"),
        sv_g=Sum("v_g"),
        sgvot=Sum("gvot"),
        sstrely=Sum("strely"),
        aperc_strel=Avg("perc_strel"),
        abuly=Avg("buly")
                        ).order_by("-sb","szapasy")

    
    return render(request,"golyapp/slovaci.html",{
        "stat":stati,
        "nation":nation_list,
        "vybratie":zvoleny_nar
                                                  })

def klub(request):
    sez_dotaz=Stats.objects.values_list("sezona",flat=True).distinct().order_by("-sezona")
    sez=[str(sezo) for sezo in sez_dotaz]

    
    vybsez=request.POST.get("sezo")
    if not vybsez and sez:
        vybsez = sez[0]
    skratky_v_sezone=Stats.objects.filter(sezona=vybsez).values_list("klub",flat=True).distinct()
    klu=CLUB.objects.filter(kod__in=skratky_v_sezone).order_by("cely_nazov_klubu")
    vybklu=request.POST.get("klub")
    if vybklu not in skratky_v_sezone and klu.exists():
        vybklu = klu.first().kod
    elif not vybklu:
        vybklu = "MTL"
    stati=Stats.objects.filter(sezona=vybsez,klub=vybklu).values("sezona","klub","id_player","pozicia","meno").annotate(
        sumazapasov=Sum("zapasy"),
        sumagolov=Sum("g"),
        sumaasistencii=Sum("a"),
        sumabodov=Sum("b"),
        sumaplus=Sum("plusminus"),
        sumav=Sum("v"),
        sumagvp=Sum("gvp"),
        sumagvo=Sum("gvo"),
        sumav_g=Sum("v_g"),
        sumagvot=Sum("gvot"),
        sumastrely=Sum("strely"),
        priemerperc=Avg("perc_strel"),
        priemerbuly=Avg("buly"),

    ).order_by("-sumabodov","sumazapasov")
    logos=Logo.objects.filter(Abbreviation=vybklu)

    
    return render(request,"golyapp/klub.html",{
        "sez":sez,
        "klu":klu,
        "vybsez":vybsez,
        "vybklu":vybklu,
        "stat":stati,
        "logo":logos
                                               })
def cze(request):
    sezonavyb=Stats.objects.values_list("sezona",flat=True).distinct().order_by("-sezona")
    sezo=[str(s) for s in sezonavyb]
    vyber=request.POST.get("sezon")
    if not vyber and sezo:
        vyber=sezo[0]


    krajina=ROK.objects.filter(krajina_nar="SVK").values_list("id_player",flat=True)
    zaver=Stats.objects.filter(sezona=vyber,id_player__in=krajina).values("sezona","meno","pozicia","id_player").annotate(
        sumazapasov=Sum("zapasy"),
        sumagolov=Sum("g"),
        sumaasistencii=Sum("a"),
        sumabodov=Sum("b"),
        sumaplus=Sum("plusminus"),
        sumav=Sum("v"),
        sumagvp=Sum("gvp"),
        sumagvo=Sum("gvo"),
        sumav_g=Sum("v_g"),
        sumagvot=Sum("gvot"),
        sumastrely=Sum("strely"),
        priemerperc=Avg("perc_strel"),
        priemerbuly=Avg("buly")


    ).order_by("-sumabodov","sumazapasov","-sumagolov")
    spodok=zaver.aggregate(
        szapasy=Sum("zapasy"),
        sg=Sum("g"),
        sa=Sum("a"),
        sb=Sum("b"),
        splusminus=Sum("plusminus"),
        sv=Sum("v"),
        sgvp=Sum("gvp"),
        sgvo=Sum("gvo"),
        sv_g=Sum("v_g"),
        sgvot=Sum("gvot"),
        sstrely=Sum("strely"),
        aperc_strel=Avg("perc_strel"),
        abuly=Avg("buly"))
    return render(request,"golyapp/cze.html",{
        "zaver":zaver,
        "sezo":sezo,
        "vyber":vyber,
        "spodok":spodok

    })
    
        
    

# Create your views here.
