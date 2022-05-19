/*
CLEANING DATA IN SQL QUERIES
*/


select *
from Housing


--Standardize Data Format
select SaleDate2, convert(date, saledate)
from Housing;

Update Housing
SET SaleDate2 = convert(date, saledate); 

alter table Housing
add SaleDate2 date;

-----------------------------------------------------------------------------------------------------------------------------

--Populte Property Address Data
Select * 
From Housing
--where PropertyAddress is null 
order by ParcelID

Select a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress, ISNULL(a.PropertyAddress, b.PropertyAddress)
From Housing a
join Housing b
on a.ParcelID = b.ParcelID 
and a.[UniqueID ] <> b.[UniqueID ]
where a.PropertyAddress is null

update a
set PropertyAddress = ISNULL(a.PropertyAddress, b.PropertyAddress)
From Housing a
join Housing b
on a.ParcelID = b.ParcelID 
and a.[UniqueID ] <> b.[UniqueID ]
where a.PropertyAddress is null


----------------------------------------------------------------------------------------------------------------------------

--Breaking out Address into Individual Columns 

Select PropertyAddress
From Housing
--where PropertyAddress is null 
--order by ParcelID

select 
substring(propertyaddress, 1, charindex(',', propertyaddress)-1) as Address,
substring(propertyaddress, charindex(',', propertyaddress)+1, len(propertyaddress)) as Address City
from housing

alter table housing 
add PropertySplitAddress Nvarchar(255)

update housing
set PropertySplitAddress = substring(propertyaddress, 1, charindex(',', propertyaddress)-1)

alter table housing 
add PropertySplitCity Nvarchar(255)

update housing
set PropertySplitCity = substring(propertyaddress, charindex(',', propertyaddress)+1, len(propertyaddress))





Select OwnerAddress
from housing

Select 
parsename (replace(owneraddress, ',', '.'), 3),
parsename (replace(owneraddress, ',', '.'), 2),
parsename (replace(owneraddress, ',', '.'), 1)
from housing

alter table housing 
add OwnerSplitAddress Nvarchar(255)

update housing
set OwnerSplitAddress = parsename (replace(owneraddress, ',', '.'), 3)

alter table housing 
add OwnerSplitCity Nvarchar(255)

update housing
set OwnerSplitCity = parsename (replace(owneraddress, ',', '.'), 2)

alter table housing 
add OwnerSplitState Nvarchar(255)

update housing
set OwnerSplitState = parsename (replace(owneraddress, ',', '.'), 1)

Select *
from housing

-----------------------------------------------------------------------------------------------------------------------------------------------------------------

--Change Y and N to Yes and No in "Sold as Vacant" field

Select distinct(SoldAsVacant), count(soldasvacant)
from housing
group by SoldAsVacant
order by 2


select SoldAsVacant, 
case when soldasvacant = 'Y' then 'Yes'
	when SoldAsVacant = 'N' then 'No'
	else soldasvacant
	end
from housing

update housing 
set SoldAsVacant = case when soldasvacant = 'Y' then 'Yes'
	when SoldAsVacant = 'N' then 'No'
	else soldasvacant
	end

----------------------------------------------------------------------------------------------------------------------------------------------------

--Removing duplicates (not standard paractice to delete data)


with RowNumCTE as(
select *, 
	ROW_NUMBER() over(
	partition by parcelid,
				propertyaddress,
				saleprice,
				saledate,
				legalreference
				order by uniqueid) row_num
from housing
--order by ParcelID
)
select *
from RowNumCTE
where row_num > 1
order by propertyaddress





--deleting duplicates
with RowNumCTE as(
select *, 
	ROW_NUMBER() over(
	partition by parcelid,
				propertyaddress,
				saleprice,
				saledate,
				legalreference
				order by uniqueid) row_num
from housing
--order by ParcelID
)
DELETE
from RowNumCTE
where row_num > 1


--------------------------------------------------------------------------------------------------------------------------------------------

--delete unused columns

select*
from housing 


alter table housing
drop column owneraddress, propertyaddress, taxdistrict, saledate