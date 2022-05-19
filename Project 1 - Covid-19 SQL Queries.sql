Select *
from PortfolioProject..CovidDeaths$ 
--where continent is not null 
order by 3,4



Select Location, date, total_cases, new_cases, total_deaths, population
from PortfolioProject..CovidDeaths$
where continent is not null 
order by 1, 2


-- Looking at total cases vs total deaths
-- Shows the likelihood of dying if you contract covid
Select Location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as DeathPercentage
from PortfolioProject..CovidDeaths$
where location like 'United States'
order by 1, 2


--Looking at total cases vs population
--Shows what percentage of population got Covid
Select Location, date, population, total_cases, (total_cases/population)*100 as PercentOfPopulationInfected
from PortfolioProject..CovidDeaths$
--where location like 'United States'
--where continent is not null 
order by 1, 2


--Looking at countries with highest infection rate compared to population
Select Location, population, max(total_cases) as HighestInfectionCount, max((total_cases/population))*100 as PercentOfPopulationInfected
from PortfolioProject..CovidDeaths$
--where location like 'United States'
--where continent is not null 
group by Location, population
order by PercentOfPopulationInfected desc

Select Location, population, date, max(total_cases) as HighestInfectionCount, max((total_cases/population))*100 as PercentOfPopulationInfected
from PortfolioProject..CovidDeaths$
--where location like 'United States'
--where continent is not null 
group by Location, population, date
order by PercentOfPopulationInfected desc

--CONTINENT NUMBERS


-- Showing countries with highest death count per population 
Select Location, max(cast(total_deaths as int)) as TotalDeathCount
from PortfolioProject..CovidDeaths$
--where location like 'United States'
where continent is not null 
group by Location
order by TotalDeathCount desc

--using location 
Select location, max(cast(total_deaths as int)) as TotalDeathCount
from PortfolioProject..CovidDeaths$
--where location like 'United States'
where continent is null 
group by location
order by TotalDeathCount desc 


--GLOBAL NUMBERS


-- total deaths and total cases in the world
Select sum(new_cases) as total_cases, sum(cast(new_deaths as int)) as total_deaths, sum(cast(new_deaths as int))/sum(new_cases)*100 as DeathPercentage
from PortfolioProject..CovidDeaths$
--where location like 'United States'
where continent is not null 
--group by date
order by 1, 2  

Select location, sum(cast(new_deaths as int)) as TotalDeathCount
From PortfolioProject..CovidDeaths$
where continent is null 
and location not in ('World', 'European Union', 'International', 'Upper middle income', 'High income', 'Lower middle income', 'Low income')
Group by location
order by TotalDeathCount desc

--Joining two tables together (Covid Deaths and Vaccinations)
Select *
From PortfolioProject..CovidVaccinations$ vac
Join PortfolioProject..CovidDeaths$ dea
	On dea.location = vac.location
	and dea.date = vac.date

-- Looking at total population vs vaccinations
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CONVERT(bigint,vac.new_vaccinations)) OVER (Partition by dea.location Order by dea.location, dea.date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
From PortfolioProject..CovidVaccinations$ vac
Join PortfolioProject..CovidDeaths$ dea
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
order by 2, 3 

--Use CTE
with PopvsVac (Continent, Location, Date, Population, new_vaccinations, RollingPeopleVaccinated)
as
(
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CONVERT(bigint,vac.new_vaccinations)) OVER (Partition by dea.location Order by dea.location, dea.date) as RollingPeopleVaccinated
From PortfolioProject..CovidVaccinations$ vac
Join PortfolioProject..CovidDeaths$ dea
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
-- order by 2, 3
)
Select *, (RollingPeopleVaccinated/Population)*100
From PopvsVac


--Creating view to store data for later isualization
Create View PercentPopulationVaccinated as 
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CONVERT(bigint,vac.new_vaccinations)) OVER (Partition by dea.location Order by dea.location, dea.date) as RollingPeopleVaccinated
From PortfolioProject..CovidVaccinations$ vac
Join PortfolioProject..CovidDeaths$ dea
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
--order by 2, 3

Select *
From PercentPopulationVaccinated

