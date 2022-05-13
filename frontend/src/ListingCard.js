import { Link } from "react-router-dom";

/** Presentational Component for each list item in list of Listings,
 * linking to their detail page
 * props: listing
 */
function ListingCard({ listing }) {
    return (
        <Link to={`/listings/${listing.id}`}>
            <div className="bg-dark my-3 d-flex p-3 rounded-3">
                {listing.imageUrl && <img className="listing-thumbnail" src={listing.imageUrl} alt={`listing-${listing.id}`}/>}
                <div className="text-start ms-5">
                    <h4>{listing.name}</h4>
                    <p>{listing.location}</p>
                    <p>{listing.price}</p>
                    <p>{listing.listingType}</p>
                    <p>{listing.detail}</p>
                </div>

            </div>
        </Link>
    )
}

export default ListingCard