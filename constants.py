from django.urls import reverse_lazy


SITE_VERSION = '0.1.0'

APP_NAME = "Hubur Way"

HOME_ACTIVITIES_OF_ANDROID = {
}

HOME_ACTIVITIES_OF_IOS = {
}

SITE_TABS = [
    {
        'display_name': 'Dashboard',
        'icon': 'home',
        'id': 'admin_dashboard',
        'link_url': reverse_lazy('admin_dashboard'),
        'visible': ['admin'],
        'active': True,
        'actions': [],
    },
    {
        'display_name': 'Dashboard',
        'icon': 'home',
        'id': 'vendor_dashboard',
        'link_url': reverse_lazy('vendor_dashboard'),
        'visible': ['vendor'],
        'active': True,
        'actions': [],
    },
    {
        'display_name': 'Categories',
        'icon': 'server',
        'id': 'categories',
        'link_url': reverse_lazy('list_categories'),
        'visible': ['admin'],
        'active': True,
        'actions': [],
    },
    {
        'display_name': 'Sub-Categories',
        'icon': 'list',
        'id': 'sub_categories',
        'link_url': reverse_lazy('list_sub_categories'),
        'visible': ['admin'],
        'active': True,
        'actions': []
    },
    {
        'display_name': 'Brands',
        'icon': 'tag',
        'id': 'brands',
        'link_url': reverse_lazy('list_brands'),
        'visible': ['admin'],
        'active': True,
        'actions': [],
    },
    {
        'display_name': 'Banners',
        'icon': 'image',
        'id': 'banners',
        'link_url': reverse_lazy('list_banners'),
        'visible': ['admin'],
        'active': True,
        'actions': [],
    },
    {
        'display_name': 'Businesses',
        'icon': 'briefcase',
        'id': 'list_business',
        'link_url': reverse_lazy('list_all_businesses'),
        'visible': ['admin'],
        'active': True,
        'actions': [],
    },
    {
        'display_name': 'Claim Request',
        'icon': 'alert-triangle',
        'id': 'claim_business',
        'link_url': reverse_lazy('list_claim_business'),
        'visible': ['admin'],
        'active': True,
        'actions': [],
    },
    {
        'display_name': 'Users',
        'icon': 'users',
        'id': 'users',
        'link_url': reverse_lazy('list_users'),
        'visible': ['admin'],
        'active': True,
        'actions': [],
    },
    {
        'display_name': 'Discounts',
        'icon': 'percent',
        'id': 'discount',
        'link_url': reverse_lazy('list_trending_discounts'),
        'visible': ['admin'],
        'active': True,
        'actions': []
    }
]