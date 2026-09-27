from app.verification import product_names_match


def test_exact_match():
    assert product_names_match(
        "Campus Sutra T-Shirt",
        "Campus Sutra T-Shirt"
    )


def test_size_suffix_match():
    assert product_names_match(
        "Campus Sutra T-Shirt",
        "Campus Sutra T-Shirt (Size L)"
    )


def test_nivea_moisturiser_variant_match():
    assert product_names_match(
        "Nivea Soft Light Moisturising Cream",
        "Nivea Soft Light Moisturiser Cream"
    )


def test_unrelated_products_do_not_match():
    assert not product_names_match(
        "Campus Sutra T-Shirt",
        "Lipton Green Tea Pure & Light"
    )