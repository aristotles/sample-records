
module SearchBar
using Dash

const resources_path = realpath(joinpath( @__DIR__, "..", "deps"))
const version = "0.0.1"

include("jl/searchbar.jl")

function __init__()
    DashBase.register_package(
        DashBase.ResourcePkg(
            "search_bar",
            resources_path,
            version = version,
            [
                DashBase.Resource(
    relative_package_path = "async-SearchBar.js",
    external_url = "https://unpkg.com/search_bar@0.0.1/search_bar/async-SearchBar.js",
    dynamic = nothing,
    async = :true,
    type = :js
),
DashBase.Resource(
    relative_package_path = "async-SearchBar.js.map",
    external_url = "https://unpkg.com/search_bar@0.0.1/search_bar/async-SearchBar.js.map",
    dynamic = true,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "search_bar.min.js",
    external_url = nothing,
    dynamic = nothing,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "search_bar.min.js.map",
    external_url = nothing,
    dynamic = true,
    async = nothing,
    type = :js
)
            ]
        )

    )
end
end
